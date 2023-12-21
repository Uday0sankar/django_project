from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here
from shop.models import Category, Product


def allchategorieos(request):
    C = Category.objects.all()
    return render(request, 'category.html', {'Category': C})


def allproducts(request, p):
    C = Category.objects.get(name=p)
    P = Product.objects.filter(category=C)
    return render(request, 'product.html', {'c': C, 'p': P})

@login_required
def item(request, p):
    P = Product.objects.get(name=p)
    return render(request, 'item.html', {'p': P})


def register(request):
    if(request.method=="POST"):
        name=request.POST['n']
        email=request.POST['e']

        pswd=request.POST['pswd']
        cpswd=request.POST['cp']

        if(cpswd==pswd):
            U=User.objects.create_user(username=name,email=email,password=pswd,)
            U.save()
            return render(request,"category.html")

        else:
            return HttpResponse("password is not matching")
    return render(request,'register.html')

def User_login(request):
    if(request.method=="POST"):
        name=request.POST['n']
        pswd=request.POST['p']
        U = authenticate(username=name, password=pswd)

        if(U):
            login(request,U)
            return redirect('shop:allChategories')
        else:
            messages.error(request,"invalid user name or password")
    return render(request,'login.html')
@login_required
def user_logout(request):
    logout(request)
    return User_login(request)

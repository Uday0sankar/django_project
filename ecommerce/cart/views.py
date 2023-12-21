from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart, Account, Order


# Create your views here.
@login_required
def add_to_cart(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=product)
        if (cart.quantity < cart.product.stock):
            cart.quantity += 1
        cart.save()
    except:
        cart = Cart.objects.create(product=product, user=u, quantity=1)
        cart.save()
    return redirect('cart:cartview')


@login_required
def cartview(request):
    u = request.user
    sum = 0
    try:

        cart = Cart.objects.filter(user=u, )

        for i in cart:
            sum = sum + ((i.quantity) * (i.product.price))



    except:
        pass
    return render(request, 'cart.html', {'c': cart, 'total': sum})


@login_required
def delete_one(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    cart = Cart.objects.get(user=u, product=product)
    try:
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass

    return redirect('cart:cartview')


def delete_cart(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=product)
        cart.delete()
    except:
        pass
    return redirect('cart:cartview')


def orderform(request):
    if (request.method == "POST"):
        accnum = request.POST['accno']
        phno = request.POST['phno']
        a = request.POST['a']
        u = request.user
        cart = Cart.objects.filter(user=u)
        total = 0
        for i in cart:
            total += i.quantity * i.product.price
        ac = Account.objects.get(accnum=accnum)
        if (ac.amount >= total):
            ac.amount -= total
            ac.save()
            for i in cart:
                o = Order.objects.create(user=u, product=i.product, phone=phno, address=a, noofitems=i.quantity,
                                         order_status="paid")
                o.save()
                i.product.stock = i.product.stock - i.quantity
                i.product.save()
            cart.delete()
            msg = "Order Placed Successfully  "
            return render(request, 'orderdetail.html', {'m': msg})
        else:
            msg = "Insufficient Amount in user Account. you cannot place order"
            return render(request, 'orderdetail.html', {'m': msg})

    return render(request, 'orderform.html')


def vieworder(request):
    u = request.user
    order = Order.objects.filter(user=u)

    return render(request, 'orderview.html', {'order': order})

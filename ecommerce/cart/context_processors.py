from cart.models import Cart


def productcount(request):
    item_count=0
    user=request.user
    try:
        cart=Cart.objects.filter(user=user)
        for i in cart:
            item_count=t=item_count+i.quantity
    except:
        item_count=0
    return {'count':item_count}


from order.models import basket, wishlist

def basket_context(request):
    data = {}
    if request.user.is_authenticated:
        basket_data = basket.objects.filter(user=request.user, is_active = True).last()
        wishlist_data = wishlist.objects.get(user=request.user)
        basket_count = basket_data.items.count()
        wishlist_count = wishlist_data.product.count()
        subtotal = 0
        basket_items = basket_data.items.all()
        for item in basket_items:
            subtotal += (item.product.product.price * item.quantity)

        data['basket'] = basket_items
        data['basket_count'] = basket_count
        data['wishlist_count'] = wishlist_count
        data['subtotal'] = subtotal    
    return data


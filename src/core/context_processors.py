from order.models import basket, wishlist
from product.models import Category

def basket_context(request):
    data = {}
    #eger sebet yoxdursa error verecek
    if request.user.is_authenticated:
        basket_data = basket.objects.filter(user=request.user, is_active = True).last()
        print(basket_data)
        wishlist_data = wishlist.objects.get(user=request.user)
        basket_count = basket_data.items.count()
        wishlist_count = wishlist_data.product.count()
        subtotal = 0
        basket_items = basket_data.items.all()
        for item in basket_items:
            subtotal += (item.product.price * item.quantity)

        print(subtotal)

        data['basket'] = basket_items
        data['basket_count'] = basket_count
        data['wishlist_count'] = wishlist_count
        data['subtotal'] = subtotal
    return data

def categories_context(request):
    categories  = Category.objects.filter(is_main = True)
    print("v---------------------------------------------------------------------")

    return  {'categories': categories}
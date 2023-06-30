from django.shortcuts import render
from django.views.generic import ListView
from order.models import wishlist, basket
from product.models import Product_version

# Create your views here.


class Wishlist(ListView):
    template_name = 'order/wishlist.html'
    model =  wishlist
    context_object_name = 'wishlist'

    def get_queryset(self):
        user_wishlist =  wishlist.objects.filter(user = self.request.user).first()
        return user_wishlist.product.all()



class ShoppingCart(ListView):
    template_name = 'order/shopping-cart.html'
    model =  basket
    context_object_name = 'b_items'

    def get_queryset(self):
        items = basket.objects.filter(user = self.request.user, is_active = True).last()
        product = items.items.all()
        subtotal = sum(item.product.product.price for item in product)
        self.product = product
        self.subtotal = subtotal
        return[]

    def get_context_data(self, **kwargs):
        context = super(ShoppingCart, self).get_context_data(**kwargs)
        context['b_items'] = self.product
        context['subtotal'] = self.subtotal

        return context


def Cart(request):
    return render(request , 'order/cart.html')

def Checkout(request):
    return render(request , 'order/checkout.html')

# def ShoppingCart(request):
#     return render(request , 'order/shopping-cart.html')






from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import basket, basket_item
from django.core import serializers

@require_POST
def Add_to_cart(request, product_id=None):
    # if product_id is None:
        # product_id = request.POST.get('product_id')
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', 1)

    if request.user.is_authenticated:
        user_basket, created = basket.objects.get_or_create(user=request.user, is_active=True)
        print(product_id)
        print('=============================================>>>>')
        product = Product_version.objects.get(pk=product_id)
        item = basket_item.objects.filter(user = request.user, product=product).first()
        
        if item:
            item.quantity = quantity
            item.save()
        else:
            new_item = basket_item.objects.create(user = request.user, product=product, )
            user_basket.items.add(new_item)

        basket_quantity = user_basket.items.count()
        print(basket_quantity)
        basket_total_price = sum(item.product.product.price * item.quantity for item in user_basket.items.all())

        product_list = basket_item.objects.filter(user=request.user)
        product_list_data = [
        {
            'picture': item.product.cover_image.url,
            'name': item.product.product.name,
            'unit_price': item.product.product.price,
            'quantity': item.quantity,
        }
        for item in product_list
    ]
        response = {
            'success': True,
            'message': 'Product added to cart successfully',
            'basket_quantity': basket_quantity,
            'basket_total_price': basket_total_price,
            'product_list': product_list_data,
            'csrf_token': request.COOKIES['csrftoken'],
        }
    else:
        response = {
            'success': False,
            'message': 'User not authenticated',
        }

    return JsonResponse(response)











# from django.http import JsonResponse

# def Add_to_cart(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             product_id = request.POST.get('product_id')
#             prod_check = Product_version.objects.get(id = product_id)
#             if prod_check:
#                 p_id = basket.items.product.id
#                 if basket.objects.filter(user = request.user.id, product_id = product_id):
#                     return JsonResponse({'status': 'Product already in cart'})

#                 else:
#                     prod_qty = request.POST.get('productQty')
#                     if prod_check.quantity >= prod_qty:
#                         basket.objects.create(user = request.user, product = product_id, quantity = prod_qty)
#                         return JsonResponse({'status': 'Product added succesfully'})
#                     else:
#                         return JsonResponse({'status': 'Not enough product'})

#             else:
#                 return JsonResponse({'status': 'Not such product found'})

#         else:
#             return JsonResponse({'status': 'Login to continue'})

#         # Return the updated count as a JSON response
#         data = {
#             'wishlist_count': wishlist_count
#         }
#         return JsonResponse(data)




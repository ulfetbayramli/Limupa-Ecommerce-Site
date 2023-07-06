from django.shortcuts import render
from django.views.generic import ListView
from order.models import wishlist, basket
from product.models import Product_version
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

#Login olmayan istifadeciler ucun ayrica mesaj yazilmalidir
class Wishlist(LoginRequiredMixin, ListView):
    template_name = 'order/wishlist.html'
    model =  wishlist
    context_object_name = 'wishlist'
    print("============================================================+++++")
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
from django.shortcuts import get_object_or_404
from django.urls import reverse


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
            'id': item.id,
            'picture': item.product.cover_image.url,
            'name': item.product.product.name,
            'unit_price': item.product.product.price,
            'quantity': item.quantity,
            'url': reverse('product_detail', args=[item.product.pk]),
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




@require_POST
def Remove_from_cart(request, product_id=None):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    basket_item_id = request.POST.get('product_id')

    if request.user.is_authenticated:
        basket_itemm = get_object_or_404(basket_item, pk = basket_item_id , user = request.user)
        basket_itemm.delete()

        print('=============================================>>>>')
        user_basket = basket.objects.filter(user=request.user, is_active=True).first()
        print(user_basket)

        basket_quantity = user_basket.items.count()
        print(basket_quantity)
        basket_total_price = sum(item.product.product.price * item.quantity for item in user_basket.items.all())

        product_list = basket_item.objects.filter(user=request.user)
        product_list_data = [
        {
            'id': item.id,
            'picture': item.product.cover_image.url,
            'name': item.product.product.name,
            'unit_price': item.product.product.price,
            'quantity': item.quantity,
            'url': reverse('product_detail', args=[item.product.pk]),
        }
        for item in product_list
    ]
        response = {
            'success': True,
            'message': 'Product removed from cart successfully',
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




#  Eger mehsul artiq wishlistde varsa elave etme.
@require_POST
def Add_to_wishlist(request, product_id=None):

    product_id = request.POST.get('product_id')
    product = Product_version.objects.get(pk=product_id)

    if request.user.is_authenticated:
        user_wishlist = wishlist.objects.get(user=request.user)
        user_wishlist.product.add(product)
        user_wishlist.save()
        
        print(user_wishlist)
        print(product_id)

        user_wishlist = wishlist.objects.get(user=request.user)
        wishlist_quantity = user_wishlist.product.count()

        response = {
            'success': True,
            'message': 'Product added to wishlist successfully',
            'wishlist_quantity': wishlist_quantity,
            'csrf_token': request.COOKIES['csrftoken'],
        }
    else:
        response = {
            'success': False,
            'message': 'User not authenticated',
        }

    return JsonResponse(response)

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from .models import wishlist, Product_version

@require_POST
def Remove_from_wishlist(request, product_id=None):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product_version, pk=product_id)

    if request.user.is_authenticated:
        user_wishlist = get_object_or_404(wishlist, user=request.user)
        user_wishlist.product.remove(product)

        wishlist_quantity = user_wishlist.product.count()
        product_list = wishlist.objects.filter(user=request.user)

        product_list_data = [
            {
                'id': item.id,
                'picture': item.product.first().cover_image.url,
                'name': item.product.first().product.name,
                'unit_price': item.product.first().product.price,
                'quantity': wishlist_quantity,
                'url': reverse('product_detail', args=[item.product.first().pk]),
            }
            for item in product_list
        ]

        response = {
            'success': True,
            'message': 'Product removed from wishlist successfully',
            'wishlist_quantity': wishlist_quantity,
            'product_list': product_list_data,
            'csrf_token': request.COOKIES['csrftoken'],
        }
    else:
        response = {
            'success': False,
            'message': 'User not authenticated',
        }

    return JsonResponse(response)

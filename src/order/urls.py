from django.urls import path
from . import views
from .views import Wishlist,  Cart, Checkout, ShoppingCart, Add_to_cart

urlpatterns = [
    path('cart', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('shopping_cart/', ShoppingCart.as_view(), name='shopping_cart'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),


    path('<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart' ),
    path('product/<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart_detail'),

    path('<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart' ),
    path('product/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart_detail'),
]
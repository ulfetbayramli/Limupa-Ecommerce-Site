from django.urls import path
from . import views
from .views import Wishlist,  Cart, Checkout, ShoppingCart, Add_to_cart, Remove_from_wishlist

urlpatterns = [
    path('cart', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),
    path('shopping_cart/', ShoppingCart.as_view(), name='shopping_cart'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),



    path('update_cart/', views.Update_cart, name='update_cart' ),
    
    # path('<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart' ),
    path('<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart' ),
    path('product/<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart_detail'),
    path('wishlist/<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart_detail'),
    path('search_by_category/<int:category_id>/<int:product_id>/add_to_cart/', views.Add_to_cart, name='add_to_cart_detail'),

    path('<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart' ),
    path('shopping_cart/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart' ),
    path('product/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart_detail'),
    path('wishlist/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart_detail'),
    path('checkout/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart_detail'),
    path('search_by_category/<int:category_id>/<int:product_id>/remove_from_cart/', views.Remove_from_cart, name='remove_from_cart_detail'),

    path('<int:product_id>/add_to_wishlist/', views.Add_to_wishlist, name='add_to_wishlist' ),
    path('product/<int:product_id>/add_to_wishlist/', views.Add_to_wishlist, name='add_to_wishlist'),
    path('search_by_category/<int:category_id>/<int:product_id>/add_to_wishlist/', views.Add_to_wishlist, name='add_to_wishlist'),

    path('wishlist/<int:product_id>/remove_from_wishlist/', views.Remove_from_wishlist, name='remove_from_wishlist' ),
    path('shipping/', views.Shippping, name='shipping'),


]
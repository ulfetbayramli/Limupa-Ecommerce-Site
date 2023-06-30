from django.urls import path
from . import views
from .views import ProductDetails, SingleProduct

urlpatterns = [
    path('compare/', views.Compare, name='compare'),
    path('product_detail', ProductDetails.as_view(), name='product_detail'),
    path('search', views.Search, name='search'),
    path('search_by_category', views.Shopleft, name='search_by_category'),
    path('product/<int:pk>', SingleProduct.as_view(), name='product_detail'),
]
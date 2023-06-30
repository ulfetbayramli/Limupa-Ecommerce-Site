from django.urls import path
from . import views
from .views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('404', views.Error404, name='error_page'),
    path('about_us/', views.AboutUS, name='about_us'),
    path('contact/', views.Contact, name='contact'),
    path('faq/', views.Faq, name='faq'),
]
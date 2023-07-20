from django.shortcuts import render

# Create your views here.
from django.db.models import Sum
from django.views.generic import ListView
from product.models import Product_version



class HomePage(ListView):
    template_name = 'core/index.html'
    model = Product_version
    context_object_name = 'products'

    # def get_queryset(self):
    #     return Product_version.objects.order_by("-date").all()[:2]

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['new_ps'] = Product_version.objects.order_by("date_added").all()[:7]
        context['bestseller_ps'] = Product_version.objects.order_by('-units_sold').all()[:7]
        context['featured_ps'] = Product_version.objects.order_by( "review_count").all()[:7]
        context['laptop'] = Product_version.objects.filter(product__category__name = 'Noutbuk' )
        context['tvaudio'] = Product_version.objects.filter(product__category__name = 'Noutbuk' )
        context['trendings'] = Product_version.objects.order_by('-units_sold').all()[:7]
        return context


from django.http import JsonResponse
from django.views import View
from .forms import SubscriberForm
from .models import Subscriber
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def SubscribeView(request):
    email = request.POST.get('emailInput')
   
    if email:
        try:
            validate_email(email)
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'You are already subscribed.'})
            else:
                Subscriber.objects.create(email=email)
                # Send confirmation message
                return JsonResponse({'success': True})
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Enter true email addres.'})
    else:
        return JsonResponse({'success': False, 'message': 'Email field is required.'})




def Error404(request):
    return render(request , 'core/404.html')

def AboutUS(request):
    return render(request , 'core/about-us.html')

def Contact(request):
    return render(request , 'core/contact.html')

def Faq(request):
    return render(request , 'core/faq.html')


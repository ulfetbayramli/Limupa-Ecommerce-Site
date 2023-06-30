from django.shortcuts import render

# Create your views here.
from .models import Product_version, Image, Product
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q


def Compare(request):
    return render(request , 'product/compare.html')


class ProductDetails(ListView):
    template_name = 'product/product-details.html'
    model = Product_version
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context['product'] = Product_version.objects.filter(id = 7)

        return context



class SingleProduct(DetailView):
    template_name = 'product/single-product.html'
    model =  Product_version
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        product = Product_version.objects.get(pk=pk)
        product.read_count += 1
        product.save()
        return product
        
    def get_context_data(self, **kwargs):
        context = super(SingleProduct, self).get_context_data(**kwargs)
        product = self.get_object()
        context['images'] = product.images.all()
        context['related_p'] = Product_version.objects.filter(Q(product__category__p_category__name = kwargs['object'].product.category.p_category) | Q(product__category__name = kwargs['object'].product.category), ~Q(pk = self.kwargs.get("pk")), ~Q(product = kwargs["object"].product)).order_by('product').all().distinct('product')[:15]

        return context



def Search(request):
    return render(request , 'product/shop-4-column.html')

def Shopleft(request):
    return render(request , 'product/shop-left-sidebar.html')





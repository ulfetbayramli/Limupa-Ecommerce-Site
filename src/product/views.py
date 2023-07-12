from django.shortcuts import render

# Create your views here.
from .models import Product_version, Image, Product
from django.views.generic import ListView, DetailView, CreateView, TemplateView
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



from .models import Category, Color

class SearchFilterPage(TemplateView):
    template_name = 'product/shop-left-sidebar.html'
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_id = self.kwargs.get('category_id')
        category = Category.objects.get(id=category_id)
        # category_id = self.request.GET.get('category')
        # subcategory_id = self.request.GET.get('subcategory')
        # color = self.request.GET.get('color')

        # Retrieve the selected category and subcategory if available
        # if category_id:
        #     category = Category.objects.get(id=category_id)
        #     context['selected_category'] = category
        #     context['selected_subcategories'] = Category.objects.filter(p_category=category)
        #     print(context)
        # if subcategory_id:
        #     context['selected_subcategory'] = Subcategory.objects.get(id=subcategory_id)

        # Retrieve the filtered products based on the selected category, subcategory, and color
        products = Product_version.objects.filter(product__category__id = category_id)
        # if category_id:
        #     products = products.filter(product__category = category)
        # if subcategory_id:
        #     products = products.filter(subcategory_id=subcategory_id)
        # if color:
        #     products = products.filter(color=color)
        context['products'] = products

        # Retrieve the available categories, subcategories, and colors for the filter options
        product_count = products.count()
        context['product_count'] = product_count
        context['category'] = category
        context['categories'] = Category.objects.filter(p_category=category)

        context['brands'] = products.values_list('product__manufacturer__name', flat=True).distinct()
        sizes = products.values_list('size__name', flat=True).distinct()
        context['sizes'] = [size for size in sizes if size is not None] 
        brands = products.values_list('product__manufacturer__name', flat=True).distinct()
        for brand in brands:
            print(brand)
        colors = Color.objects.filter(id__in=products.values_list('color', flat=True).distinct())
        context['colors'] = colors
        
        return context

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        color = request.POST.get('color')

        # Perform additional filtering based on the AJAX request data
        products = Product.objects.all()
        if category_id:
            products = products.filter(category_id=category_id)
        if subcategory_id:
            products = products.filter(subcategory_id=subcategory_id)
        if color:
            products = products.filter(color=color)

        # Serialize the filtered products to JSON
        products_json = [{'name': product.name, 'description': product.description} for product in products]

        return JsonResponse({'products': products_json})
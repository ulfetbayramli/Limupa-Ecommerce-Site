from django.shortcuts import render

# Create your views here.
from .models import Product_version, Image, Product, Manufacturer
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
        print(product.read_count)
        product.read_count += 1
        print(product.read_count)
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

    def get_parent_category(self, categories):
        # Find the common parent category among a list of categories
        # Assumes that categories are related in a hierarchical manner
        parent_category = None
        for category in categories:
            print("evvel")
            if not category.p_category:  # If the category has no parent, it's the top-level category
                parent_category = category
                break
        return parent_category


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_id = self.kwargs.get('category_id')
        category = None
        products = Product_version.objects.filter(product__category=category)


        if category_id:
            category = Category.objects.get(id=category_id)
            categories = Category.objects.filter(p_category=category)
            products = Product_version.objects.filter(product__category=category)



        search_query = self.request.GET.get('search')

        if search_query:

            exact_category = Category.objects.filter(name__iexact=search_query)
            exact_manufacturer = Manufacturer.objects.filter(name__iexact=search_query)
            if exact_category.exists():
                print("categoryyyyyyyyyyyyy")
                products = Product_version.objects.filter(product__category__in=exact_category)
                category = exact_category.first()
                categories = Category.objects.filter(p_category=category)

            if not products.exists():

                if exact_manufacturer.exists():
                    print("manuuuuuuuuuuufacturer")
                    products = Product_version.objects.filter(product__manufacturer__in=exact_manufacturer)
                    category = exact_manufacturer.first()
                    categories = Category.objects.filter(product_category__product_version__in=products).distinct()
                    print("11111111111111111", categories)

                else:
                    products = Product_version.objects.filter(Q(product__name__icontains=search_query) | Q(product__description__icontains=search_query))
                    categories = Category.objects.filter(product_category__product_version__in=products).distinct()
                    category = self.get_parent_category(categories)

                    print("2222222222222222",categories)

                # if related_categories:
                #     categories = related_categories


        context['products'] = products

        product_count = products.count()
        context['product_count'] = product_count
        context['category'] = category
        context['categories'] = categories

        context['brands'] = products.values_list('product__manufacturer__name', flat=True).distinct()
        sizes = products.values_list('size__name', flat=True).distinct()
        context['sizes'] = [size for size in sizes if size is not None] 
        brands = products.values_list('product__manufacturer__name', flat=True).distinct()
        for brand in brands:
            print(brand)
        colors = Color.objects.filter(id__in=products.values_list('color', flat=True).distinct())
        context['colors'] = colors
        
        return context







from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count

class ApplyFilters(View):
    def post(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
    
        
        selected_categories = request.POST.getlist('categories[]')
        selected_brands = request.POST.getlist('brands[]')
        selected_sizes = request.POST.getlist('sizes[]')
        selected_colors = request.POST.getlist('colors[]')
        sort_by_option = request.POST.get('sort_by', 'trending')

        if category_id:
            products = Product_version.objects.filter(product__category__id=category_id)
            print(products)
        else:
            # products = Product_version.objects.all()
            if selected_categories:
                products = Product_version.objects.filter(id__in=selected_categories)
                print(products) 
            else:
                products = Product_version.objects.all()

        if selected_brands:
            products = products.filter(product__manufacturer__name__in=selected_brands)
        if selected_sizes:
            products = products.filter(size__name__in=selected_sizes)
        if selected_colors:
            products = products.filter(color__name__in=selected_colors)

        if sort_by_option == 'price-asc':
            products = products.order_by('price')
            print(products)
        elif sort_by_option == 'price-desc':
            products = products.order_by('-price')
        elif sort_by_option == 'newest':
            products = products.order_by('-date_added')
        elif sort_by_option == 'bestsellers':
            products = products.order_by('-units_sold')
        elif sort_by_option == 'like':
            products = products.annotate(like_count=Count('wishlist_product')).order_by('-like_count')
        elif sort_by_option == 'review':
            products = products.order_by('-review_count')


        print(selected_brands, selected_colors)
        product_count = products.count()

        product_list = [
        {
            'id': product.id,
            'picture': product.cover_image.url,
            'name': product.product.name,
            'price': product.price,
            'url': reverse('product_detail', args=[product.product.pk]),
        }
        for product in products
    ]
        response = {
            'success': True,
            'message': 'Products filtered',
            'product_count': product_count,
            'products': product_list,
            'csrf_token': request.COOKIES['csrftoken'],
        }

        return JsonResponse(response)
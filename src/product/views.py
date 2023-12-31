from django.shortcuts import render

# Create your views here.
from .models import Product_version, Image, Product, Manufacturer
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count


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
        context['p_versions'] = Product_version.objects.filter(product=product.product).order_by('id')
        print(Product_version.objects.filter(product = product.product), "333333333333333333333333333333333333333333333333333")
        context['images'] = product.images.all()
        context['related_p'] = Product_version.objects.filter(Q(product__category__p_category__name = kwargs['object'].product.category.p_category) | Q(product__category__name = kwargs['object'].product.category), ~Q(pk = self.kwargs.get("pk")), ~Q(product = kwargs["object"].product)).order_by('product').all().distinct('product')[:15]

        return context



def Search(request):
    return render(request , 'product/shop-4-column.html')

def Shopleft(request):
    return render(request , 'product/shop-left-sidebar.html')



from .models import Category, Color, Storage

def get_subcategories(category):
    subcategories = []
    for subcategory in category.parent_category.all():
        subcategories.append(subcategory)
        subcategories.extend(get_subcategories(subcategory))
    return subcategories

class SearchFilterPage(TemplateView):
    template_name = 'product/shop-left-sidebar.html'

    def get_parent_category(self, categories):
        parent_category = None
        for category in categories:
            if not category.p_category:
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
            if not products:
                subcategories = get_subcategories(category)
                print(subcategories)
                categories = subcategories
                products = Product_version.objects.filter(product__category__in=subcategories)



        search_query = self.request.GET.get('search')

        if search_query:

            exact_category = Category.objects.filter(name__iexact=search_query)
            exact_manufacturer = Manufacturer.objects.filter(name__iexact=search_query)
            if exact_category.exists():
                products = Product_version.objects.filter(product__category__in=exact_category)
                category = exact_category.first()
                categories = Category.objects.filter(p_category=category)

            if not products.exists():

                if exact_manufacturer.exists():
                    products = Product_version.objects.filter(product__manufacturer__in=exact_manufacturer)
                    category = exact_manufacturer.first()
                    categories = Category.objects.filter(product_category__product_version__in=products).distinct()

                else:
                    products = Product_version.objects.filter(Q(product__name__icontains=search_query) | Q(product__description__icontains=search_query))
                    categories = Category.objects.filter(product_category__product_version__in=products).distinct()
                    category = self.get_parent_category(categories)


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
        storages = Storage.objects.filter(id__in=products.values_list('storage', flat=True).distinct())
        context['colors'] = colors
        context['storages'] = storages
        
        return context







class ApplyFilters(View):
    def post(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
    
        
        selected_products = request.POST.getlist('products[]')
        selected_storages = request.POST.getlist('storages[]')
        minPrice = request.POST.get('minPrice')
        maxPrice = request.POST.get('maxPrice')
        selected_brands = request.POST.getlist('brands[]')
        selected_sizes = request.POST.getlist('sizes[]')
        selected_colors = request.POST.getlist('colors[]')
        sort_by_option = request.POST.get('sort_by', 'trending')

        # if category_id:
        #     products = Product_version.objects.filter(product__category__id=category_id)
        #     print(products,"111111")
        # else:
            # products = Product_version.objects.all()
        if selected_products:
            products = Product_version.objects.filter(id__in=selected_products)
            print(products,"222222222222") 
        else:
            products = Product_version.objects.all()

        if selected_brands:
            products = products.filter(product__manufacturer__name__in=selected_brands)
        if selected_sizes:
            products = products.filter(size__name__in=selected_sizes)
        if selected_colors:
            products = products.filter(color__name__in=selected_colors)
        if selected_storages:
            products = products.filter(storage__name__in=selected_storages)
        if minPrice:
            products = products.filter(price__gte=minPrice)
        if maxPrice:
            products = products.filter(price__lte = maxPrice)

        if sort_by_option == 'price-asc':
            products = products.order_by('price')
            print(products,"33333333333")
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


        print(selected_brands, selected_storages)
        product_count = products.count()

        product_list = [
        {
            'id': product.id,
            'picture': product.cover_image.url,
            'name':  f"{product.product.name}{f' {product.storage.name}' if product.storage else ''}{f'  {product.color.name}' if product.color else ''}",
            'price': product.price,
            'category':  product.product.category.name if product.product.category else None,
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
from order.models import basket, wishlist
from product.models import Category

def basket_context(request):
    data = {}
    #eger sebet yoxdursa error verecek
    if request.user.is_authenticated:
        basket_data, _ = basket.objects.get_or_create(user=request.user, is_active=True)
        print(basket_data)
        wishlist_data, _ = wishlist.objects.get_or_create(user=request.user)
        basket_count = basket_data.items.count()
        wishlist_count = wishlist_data.product.count()
        subtotal = 0
        basket_items = basket_data.items.all()
        for item in basket_items:
            subtotal += (item.product.price * item.quantity)

        print(subtotal)

        data['basket'] = basket_items
        data['basket_count'] = basket_count
        data['wishlist_count'] = wishlist_count
        data['subtotal'] = subtotal
    return data

def categories_context(request):
    categories  = Category.objects.filter(is_main = True)
    print("v---------------------------------------------------------------------")

    return  {'categories': categories}


def get_subcategories(category):
    subcategories = []
    for subcategory in category.parent_category.all():
        subcategories.append(subcategory)
        subcategories.extend(get_subcategories(subcategory))
    return subcategories

def category_context(request):
    # main_categories = Category.objects.filter(is_main=True)
    telefone_category = Category.objects.get(name='telefon')
    computer_category = Category.objects.get(name='Komputerler')
    sc_category = Category.objects.get(name='Smart Cihazlar')
    gc_category = Category.objects.get(name='Oyun konsolları')
    tv_category = Category.objects.get(name='TV, audio, video')
    

    telefone_subcategories = get_subcategories(telefone_category)
    computer_subcategories = get_subcategories(computer_category)
    sc_subcategories = get_subcategories(sc_category)
    gc_subcategories = get_subcategories(gc_category)
    tv_subcategories = get_subcategories(tv_category)

    print(telefone_subcategories, "sadfghgfsaddfrgthyjuiolujytrgedswertyuiouybvfcdxsdfergthyjuklikmujynhtbgvfcdxsdefrgtyhujikoumyjnhtbgvfdsxdfrgthyjuk")

    context = {
        # 'main_categories': main_categories,
        'telefone_subcategories': telefone_subcategories,
        'computer_subcategories': computer_subcategories,
        'sc_subcategories': sc_subcategories,
        'gc_subcategories': gc_subcategories,
        'tv_subcategories': tv_subcategories,
    }

    return context

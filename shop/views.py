from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender


# This function view will display all the available products
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) # This will only allow products listed as available to appear
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category) # This will collect available products from a specified category
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


# This function view will display an individual product with its description
def product_detail(request, id, slug): 
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True) # This will get a single product, using both ID and Slug. It will work with primary key alone, 
                                                # but this method allows for URL pattern building

    cart_product_form = CartAddProductForm()

    # The recommender is called here to list suggestions on the product detail screen.
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    # Here are the list of items send for use in the view, the product, handling input information via the form
    # and the list of calculated recommended products itself.
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})

# import weasyprint - will cause an error if active, incompatibility issues in progress
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from shop.recommender import Recommender

# This function creates an order with a POST request from the order creation form which it calls.
# It handles a coupon, saves the contents, then creates an OrederItem object with the details.
# The list of products is handed to the recommender to update the matrix.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                                         # name=item['name'])
            # last line 'name' ^^^ is addtional, in order to list names dircetly for recommender, as oppsed to a separate query
            # This is non-functional at present, it will only return a list of numbers as a foriegn key as opposed to one name
            # of the product as originally intended.

            # cart_product_objects = [item['product'] for item in cart] - original iteration causes a tuple unpacking error.
            cart_product_objects = [item['product'] for item in cart]
            print(type(cart_product_objects))
            print(cart_product_objects)

            for item in cart_product_objects:
                print(item)

            # Update recommender

            r = Recommender()
            r.products_bought(cart_product_objects)

            # clear the cart
            cart.clear()

            # The system to send a confirmation email below is disabled due to system incompatibility.
            # launch asynchronous task
            # order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment. Original version passed the objects list to the payment section,
            # however this caused multiple errors through a problem GET request that were best resolved here.
            return redirect(reverse('payment:process')) #, cart_product_objects
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
# redirect information: https://realpython.com/django-redirects/

# decorated function to allow access to order details for an admin user
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

# decorated function to allow access to order details for an admin user, 
# included despite PDF billing functionality not working through incompatibility issues
# with out of date OS.
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    # This PDF readaer is disabled as OS incompatible.
    # weasyprint.HTML(string=html).write_pdf(response,
    #     stylesheets=[weasyprint.CSS(
    #         settings.STATIC_ROOT + 'css/pdf.css')])
    return response

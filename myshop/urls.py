from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# These are the basic navigation URLS for the shop.  

urlpatterns = [
    path('admin/', admin.site.urls),									# navigation to the admin page and superuser login
    path('cart/', include('cart.urls', namespace='cart')),				# "" to the shopping car
    path('orders/', include('orders.urls', namespace='orders')),		# "" to the orders page
    path('payment/', include('payment.urls', namespace='payment')),		# "" to the payment page 
    path('coupons/', include('coupons.urls', namespace='coupons')),		# leads to the coupons creation page
    path('', include('shop.urls', namespace='shop')),					# The home page
]


# The following code is serving static files as part of development.
# This is a work in progress and for the production environment
# A different strategy will be used for the active site.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

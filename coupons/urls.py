from django.urls import path
from . import views

app_name = 'coupons'

# There is only one url pattern for the Coupon app
urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
]

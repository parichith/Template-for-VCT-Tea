from django.urls import path
from . import views

# This app identifies itself as 'orders'
app_name = 'orders'

# These are the url patterns used to navigate the views in this app
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]

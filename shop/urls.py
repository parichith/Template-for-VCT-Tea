from django.urls import path
from . import views

# the shop app is named 'shop'
app_name = 'shop'

# Here are the URL patterns for the shop app.
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'), # a slug only url lists by category
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'), # a primary key and slug lists a single product for detail purposes
]

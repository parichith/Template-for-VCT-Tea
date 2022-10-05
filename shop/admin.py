from django.contrib import admin
from .models import Category, Product


# This allows the content of the defined models to be edited in the admin screen by a superuser.
# It allows new products and categories of products to be created on the admin screen.

# This class allows new categores to be created 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

#This class allows new products to be created
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # this field allows multiple list editing from the admin screen by a superuser
    prepopulated_fields = {'slug': ('name',)}


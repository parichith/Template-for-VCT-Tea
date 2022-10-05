from django.db import models
from django.urls import reverse

# This class deliminates what kind of product or tea in this case we are using.
class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug]) # This collects a url for category


# This class holds all the details of each tea product.
class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)      # Foriegn key to Category model, one category, many products
    name = models.CharField(max_length=200, db_index=True)      # The product name
    slug = models.SlugField(max_length=200, db_index=True)      # The slug for URL use
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)                       # The product image storage
    description = models.TextField(blank=True)                  # The description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)# The price of the product is stored in a decimal field with two decimal places
    available = models.BooleanField(default=True)               # This boolean field enabled a product to be enabled or disabled in accordance with use
    created = models.DateTimeField(auto_now_add=True)           # Records when the product was created
    updated = models.DateTimeField(auto_now=True)               # Records when the product details were changed 

    # The Meta class conflates the primary key and slug field for indexing purposes
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug]) # This collects a url for products.

# The reverse method switches objects around in a list, used here for url assembley
# https://www.geeksforgeeks.org/python-list-reverse/

from django import forms
from .models import Order

# This class holds customer details against an order instance
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'post_code', 'country']
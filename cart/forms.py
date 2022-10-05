from django import forms

# This limits the input form to selections of one to twenty products
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

# This form collects quanitity and manages updates with an override, hidden from the user,
# that manages existing products in the cart or updates to this figure
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

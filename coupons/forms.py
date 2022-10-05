from django import forms
# from django.utils.translation import gettext_lazy as _

# class sets the coupon code to a char field
class CouponApplyForm(forms.Form):
    code = forms.CharField()

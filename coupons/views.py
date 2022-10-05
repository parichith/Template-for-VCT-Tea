from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

# decorator requires a POST request to operate the function.
# This function collects the current time, the appropriate input form, performs validation,
# and creates the Coupon object. The coupon is active between the dates set.

# The coupon does not effect the recommender system directly, but is presetn here for development
# purposes. The functionality is to be increased to give discounts to teas that require promotion,
# not currently part of the current functionality which is just a general discount.
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

from django.urls import path
from . import views

# This app is named here 'payment'
app_name = 'payment'

# Here are the url patterns used in the payment app.
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]

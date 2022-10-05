# from celery import task
from django.core.mail import send_mail
from .models import Order

# This function is to to send an e-mail notification when an order is successfully created.
# This is currently non-functional due to incompatibility, the function never gets called.

# @task - decorater is non-functional and is part of the ongoing PDF OS compatibility error
def order_created(order_id):

    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent

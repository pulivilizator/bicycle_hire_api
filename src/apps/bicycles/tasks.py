from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.bicycles.models import Rental


@shared_task
def send_rental_ended_mail(rental_id):
    try:
        rental = Rental.objects.get(id=rental_id)
    except Rental.DoesNotExist:
        return
    context = {
        'current_user': rental.user,
        'total_price': rental.total_price
    }

    email_html_message = render_to_string('email/rental_ended.html', context)
    email_plaintext_message = render_to_string('email/rental_ended.txt', context)

    msg = EmailMultiAlternatives(
        'Оплата заказа',
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [rental.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
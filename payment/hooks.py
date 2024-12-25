from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings


# This function will be called when a payment is confirmed.
@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    # Grab the info that PayPal sends
    paypal_object = sender
    print(paypal_object)
    print(f'Amount Paid: {paypal_object.mc_gross}')

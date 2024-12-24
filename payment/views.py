from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingAddressForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItems
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime
# Import PayPal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid  # unique user id for duplicate orders


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItems.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == 'true':
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                messages.success(request, "Order marked as shipped!")
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
                # Save the changes
                messages.success(request, "Order marked as not shipped!")
            return redirect('home')
        return render(request, 'payment/orders.html', {"order": order, "items": items})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # grab date and time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=True, date_shipped=now)
            # redirect
            messages.success(request, "Order marked as shipped!")

            return redirect('home')
        return render(request, "payment/not_shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # grab date and time
            now = datetime.datetime.now()
            # update order
            order.update(shipped=False)
            # redirect
            messages.success(request, "Order marked as unshipped!")

            return redirect('home')
        return render(request, "payment/shipped_dash.html", {"orders": orders})
    else:
        messages.success(request, "Access Denied!")
        return redirect('home')


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)

        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['Shipping_full_name']
        email = my_shipping['Shipping_email']

        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['Shipping_address1']}\n{my_shipping['Shipping_address2']}\n" \
                           f"{my_shipping['Shipping_city']}\n{my_shipping['Shipping_state']}\n" \
                           f"{my_shipping['Shipping_zip_code']}\n{my_shipping['Shipping_country']}\n"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Create Order Items
            # Get the Order ID
            order_id = create_order.pk

            # Get Product Info
            for product in cart_products():
                # Get Product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id,
                                                       price=price, quantity=value, user=user)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            # Delete cart from database(old cart)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database(old_cart)
            current_user.update(old_cart="")
            messages.success(request, "Order Placed!")
            return redirect('home')
        else:
            # not logged in
            create_order = Order(full_name=full_name, email=email,
                                 shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Create Order Items
            # Get the Order ID
            order_id = create_order.pk

            # Get Product Info
            for product in cart_products():
                # Get Product ID
                product_id = product.id
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id,
                                                       price=price, quantity=value)
                        create_order_item.save()

            messages.success(request, "Order Placed!")
            return redirect('home')
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Get the host
        host = request.get_host()
        # Create PayPal Form Dictionary
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Jewelry Order',
            'no_shipping': '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
            'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
            'cancel_return': 'https://{}{}'.format(host, reverse("payment_failed"))

        }

        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        # Check to see if user is logged in
        if request.user.is_authenticated:
            # Get the Billing Information
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products,
                                                                 "quantities": quantities, "totals": totals,
                                                                 "shipping_form": request.POST,
                                                                 "billing_form": billing_form,
                                                                 "paypal_form": paypal_form,
                                                                 })
        else:
            # Not Logged in
            # Get The Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products,
                                                                 "quantities": quantities, "totals": totals,
                                                                 "shipping_form": request.POST,
                                                                 "billing_form": billing_form,
                                                                 "paypal_form": paypal_form,
                                                                 })

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products": cart_products,
                                                             "quantities": quantities, "totals": totals,
                                                             "shipping_form": shipping_form})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as Logged-in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                         "quantities": quantities, "totals": totals,
                                                         "shipping_form": shipping_form})
    else:
        # Checkout as Guest user
        shipping_form = ShippingAddressForm(request.POST or None)

        return render(request, "payment/checkout.html", {"cart_products": cart_products,
                                                         "quantities": quantities, "totals": totals,
                                                         "shipping_form": shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def payment_failed(request):
    return render(request, 'payment/payment_failed.html', {})

from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    Shipping_full_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}), required=True, )
    Shipping_email = forms.CharField(label="",
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Email Address'}), required=True, )
    Shipping_address1 = forms.CharField(label="",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Address1'}),
                                        required=True, )
    Shipping_address2 = forms.CharField(label="",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Address2'}),
                                        required=False, )
    Shipping_city = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                                    required=True, )
    Shipping_state = forms.CharField(label="",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                                     required=False, )
    Shipping_zip_code = forms.CharField(label="",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                                        required=False, )
    Shipping_country = forms.CharField(label="",
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Country'}),
                                       required=True, )

    class Meta:
        model = ShippingAddress
        fields = ['Shipping_full_name', 'Shipping_email', 'Shipping_address1', 'Shipping_address2', 'Shipping_city',
                  'Shipping_state', 'Shipping_zip_code', 'Shipping_country']
        exclude = ['user', ]


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name On Card'}), required=True, )
    card_number = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required=True, )
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Expiration Date'}), required=True, )
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CVV Code'}), required=True, )
    card_address1 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'}), required=True, )
    card_address2 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}), required=False, )
    card_city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing City'}), required=True, )
    card_state = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=True, )
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}), required=True, )
    card_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Country'}), required=True, )

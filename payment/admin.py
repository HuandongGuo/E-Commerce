from django.contrib import admin
from .models import ShippingAddress, Order, OrderItems
from django.contrib.auth.models import User

# Register the model on the admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)


# Create an OderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0


# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address",
              "amount_paid", "date_ordered", "shipped",
              "date_shipped", "invoice", "paid"]
    inlines = [OrderItemInline]


# Unregister Order Model
admin.site.unregister(Order)

# Register Order Model with our custom OrderAdmin
admin.site.register(Order, OrderAdmin)

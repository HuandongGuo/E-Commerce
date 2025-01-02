from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)



class OrderAdmin(admin.ModelAdmin):
    list_display = ["_product", "customer", "status"]
    list_filter = ["status"]

    def _product(self, order):
        url = (reverse("admin:store_product_changelist") +
               "?" +
               urlencode({
                   "id": order.product.id
               }))
        return format_html("<a href='{}'>{}</a>", url, order.product)
    

admin.site.register(Order, OrderAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username"]

    # make the displayed username a link to where the user can be found
    def username(self, profile):
        url = (reverse("admin:auth_user_changelist") +
               "?" +
               urlencode({
                   "id": profile.user.id
               }))
        return format_html("<a href='{}'>{}</a>", url, profile)

admin.site.register(Profile, ProfileAdmin)





# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]


# Unregister the old way
admin.site.unregister(User)

# Register the new way
admin.site.register(User, UserAdmin)

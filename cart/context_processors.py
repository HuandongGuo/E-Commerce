from .cart import Cart


# Create context processor so our cart can work on all pages of site
def cart(request):
    # Return the default data of our Cart
    return {'cart': Cart(request)}

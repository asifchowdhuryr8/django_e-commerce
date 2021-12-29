from django.db import models
from store.models import Product, Variation
from account.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=500, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # user field added so that we can know the user who has added the product to the cart
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # ManyToManyField is used so that it can handle the situation when one product has multiple variations.
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.product

    def sub_total(self):
        """Returns total price for individual cart item"""
        return self.product.price * self.quantity

# NOTE: Use __str__ only when you sure that there never will be non-ASCII characters in the stringified output

# NOTE: Use __unicode__ only when you sure that there will be ASCII characters in the stringified output.

# ERROR: Whenever you encounter this error message( __str__ returned non-string) then you can use __unicode__ to solve the problem

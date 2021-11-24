from django.db import models
from category.models import Category
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    price = models.IntegerField()
    image = models.ImageField(
        upload_to='images/products', null=True, blank=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    #  NOTE:    auto_now_add=True: When the model is created, the date will be set to the current date and time. It won't update the date when the model is updated.
    # NOTE:    auto_now=True: When the model is saved, the date will be set to the current date and time. It will update the date when the model is updated.

    def __str__(self):
        return self.name

    def get_single_product_url(self):
        return reverse('store:product-detail', args=[self.category.slug, self.slug])
    # You can use this mehtod if you don't want to use product.category.slug syntax in the template. just use product.get_single_product_url in the href attribute of the link.

    # I have used product.category.slug product.slug syntax in the index file and get_single_product_url syntax in the store.html file


class VariationManager(models.Manager):

    def get_color(self):
        return super(VariationManager, self).filter(variation='color', is_active=True)

    def get_size(self):
        return super(VariationManager, self).filter(variation='size', is_active=True)

# You can use this class to get the color and size variations of the product. You can create this methods inside the Variation class too. But it is better to create a class for this to keep the code clean.


class Variation(models.Model):
    VARIATION_CHOICES = (
        ('color', 'color'),
        ('size', 'size'),
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variations')
    variation = models.CharField(max_length=50, choices=VARIATION_CHOICES)
    variation_value = models.CharField(max_length=50)
    # If you want to remove from a product then just set the is_active to False.
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # Inform the Variation class that VariationManager is related with it. Or you can say that connecting the VariationManager with the Variation class.
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

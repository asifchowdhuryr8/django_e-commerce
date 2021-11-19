from django.db import models
from category.models import Category

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

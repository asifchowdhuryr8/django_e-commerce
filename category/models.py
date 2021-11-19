from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    image = models.ImageField(
        upload_to='images/categories', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_slug_url(self):
        return reverse('store:products-by-category', args=[self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        # By default python convert model name to lowercase and pluralize it. Here I have used category as the model name and django convert in to categorys with an additional s to make it plural. So if you want to manually change the plural model name then use above code.

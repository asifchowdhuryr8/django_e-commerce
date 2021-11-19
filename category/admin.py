from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    # slug field will be automatically populated with the value of the name field
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


# Register your models here.
admin.site.register(Category, CategoryAdmin)

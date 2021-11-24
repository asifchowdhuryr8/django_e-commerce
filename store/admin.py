from django.contrib import admin
from .models import Product, Variation
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'stock',
                    'is_available', 'category', 'created_date', 'modified_date']


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation', 'variation_value', 'is_active']
    # Directly edit is_active field from admin page.
    list_editable = ('is_active',)
    # Add filter for product, variation and variation_value in the admin page
    list_filter = ('product', 'variation', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'last_login', 'date_joined', 'is_admin')    # list_display is used to display the fields in the admin page.
    list_display_links = ('email', 'first_name', 'last_name')   # list_display_links is used to make the fields clickable.
    readonly_fields = ('last_login', 'date_joined') # readonly_fields is used to make the fields read only.
    ordering = ('-date_joined',)    # ordering is used to order the fields in the admin page.


    # REQUIRED FIELDS(Since we are using our custom authentication model otherwise don't need them.)

    filter_horizontal = ()  # filter_horizontal is used to filter the fields in the admin page.
    list_filter = ()    # list_filter is used to filter the fields in the admin page.
    fieldsets = ()  # fieldsets is used to group the fields in the admin page.  If you don't specify any fieldsets then it will display all the fields in the admin page.

# Register your models here.
admin.site.register(Account, AccountAdmin)  # Passing the AccountAdmin class so that it applies the customizations to the Account model.
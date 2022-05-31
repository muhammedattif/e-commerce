from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Vendor, Address

class UserConfig(UserAdmin):
    model = User

    list_filter = ('email', 'phone_number', 'is_active', 'is_staff', 'reg_as_vendor')
    ordering = ('-date_joined',)
    list_display = ('email', 'phone_number',
                    'is_active', 'is_staff')

    fieldsets = (
        ("User Information", {'fields': ('email', 'phone_number', 'first_name', 'last_name', 'agent_name', 'city', 'district', 'location', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'reg_as_vendor', 'is_superuser', 'groups', 'user_permissions')}),
    )



class VendorConfig(admin.ModelAdmin):
    model = Vendor

    list_filter = ('is_active', 'user__email')
    list_display = ('user', 'is_active')



class AddressConfig(admin.ModelAdmin):
    model = Address

    list_filter = ('user', 'locality', 'city', 'state', 'zipcode')
    list_display = ('user', 'locality', 'city', 'state', 'zipcode')


# Register your models here.
admin.site.register(User, UserConfig)
admin.site.register(Vendor, VendorConfig)
admin.site.register(Address, AddressConfig)

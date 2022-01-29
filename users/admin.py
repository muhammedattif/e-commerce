from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Student, Teacher, VendorProfile, CustomerProfile, Address

class UserConfig(UserAdmin):
    model = User

    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff')

    fieldsets = (
        ("User Information", {'fields': ('email', 'username', 'first_name', 'last_name', 'avatar', 'location')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_vendor', 'is_superuser', 'groups', 'user_permissions')}),
    )

class StudentConfig(admin.ModelAdmin):
    model = Student

    list_filter = ('user', 'major', 'academic_year', 'year_in_school')
    list_display = ('user', 'major', 'academic_year', 'year_in_school')

    fieldsets = (
        ("Student Account", {'fields': ('user', )}),
        ('Education', {'fields': ('major', 'academic_year', 'year_in_school')}),
    )

class TeacherConfig(admin.ModelAdmin):
    model = Teacher

    list_filter = ('major', )
    list_display = ('user', 'major')

class VendorConfig(admin.ModelAdmin):
    model = Teacher

    list_filter = ('user', )
    list_display = ('user',)

class AddressConfig(admin.ModelAdmin):
    model = Address

    list_filter = ('user', 'locality', 'city', 'state', 'zipcode')
    list_display = ('user', 'locality', 'city', 'state', 'zipcode')


# Register your models here.
admin.site.register(User, UserConfig)
admin.site.register(Student, StudentConfig)
admin.site.register(Teacher, TeacherConfig)
admin.site.register(VendorProfile, VendorConfig)
admin.site.register(CustomerProfile)
admin.site.register(Address, AddressConfig)

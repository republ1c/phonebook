from django.contrib import admin
from phonebook.models import User
from phonebook.models import PhoneNumber


class PhoneBookInline(admin.StackedInline):
    model = PhoneNumber
    extra = 0


# @admin.register(User)
class PhoneNumberAdmin(admin.ModelAdmin):
    fields = ['user_name', 'user_surname', 'user_email']
    inlines = [PhoneBookInline]


admin.site.register(User, PhoneNumberAdmin)
# admin.site.register(User)
# admin.site.register(PhoneNumber)

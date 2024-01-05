from django.contrib import admin

from users.models import User, UserConfirmation


# Register your models here.

class ModelAminUser(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'phone_number']
admin.site.register(User,ModelAminUser)
admin.site.register(UserConfirmation)
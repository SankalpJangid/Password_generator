import imp
from django.contrib import admin
from .models import UserDetails, UserPasswords

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(UserPasswords)
from django.contrib import admin
from .models import UserProfile, Purchase


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Purchase)

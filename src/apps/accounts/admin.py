from django.contrib import admin
from .models import UserProfile, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'ticket', 'creation_time', )


admin.site.register(UserProfile)
admin.site.register(Purchase, PurchaseAdmin)

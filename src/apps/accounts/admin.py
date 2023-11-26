from django.contrib import admin
from .models import UserProfile, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', )


admin.site.register(UserProfile)
admin.site.register(Purchase, PurchaseAdmin)

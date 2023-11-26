from django.contrib import admin
from .models import UserProfile, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', )
    def delete_queryset(self, request, queryset):
        print('==========================delete_queryset==========================')
        print(request)
        print(queryset)
        for i in queryset:
            Purchase.delete(i)
        queryset.delete()

        print('==========================delete_queryset==========================')


admin.site.register(UserProfile)
admin.site.register(Purchase, PurchaseAdmin)

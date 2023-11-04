from django.contrib import admin
from .models import Event, Ticket


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket)

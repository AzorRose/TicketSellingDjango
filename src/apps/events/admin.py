from django.contrib import admin
from .models import Event, Ticket


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "date"]
    readonly_fields = ('people_count', )


class TicketAdmin(admin.ModelAdmin):
    search_fields = ["event__name", "price"]


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)

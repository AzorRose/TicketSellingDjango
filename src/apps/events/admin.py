from django.contrib import admin
from .models import Event, Ticket, Booked_Places


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "date"]
    readonly_fields = (
        "people_count",
        "booked_balcony",
        "booked_sitting",
        "booked_dance_floor",
    )


class TicketAdmin(admin.ModelAdmin):
    search_fields = ["event__name", "price"]


class Booked_PlacesAdmin(admin.ModelAdmin):
    readonly_fields = ["available"]
    search_fields = ["event", "spot", "spot_num"]


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Booked_Places, Booked_PlacesAdmin)

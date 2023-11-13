from django.shortcuts import render
from .models import Event, Ticket
from apps.accounts.models import UserProfile
from django.views import View


# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        profile = UserProfile.objects.all()
        ticket = Ticket.objects.all()
        return render(request, "events/index.html", context={"profile": profile, "event": event, "ticket": ticket})


class EventView(View):
    def get(self, request, *args, **kwargs):
        # Получает путь из запроса и возвращает информацию о конкретном событии, которому соответствует этот путь
        slug_match = request.path[request.path.rfind("/") + 1:]
        event = Event.objects.get(slug=slug_match)
        ticket = Ticket.objects.filter(event=event)
        if event:
            return render(request, "events/event.html", context={"event": event, "ticket": ticket})

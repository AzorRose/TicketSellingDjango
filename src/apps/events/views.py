from django.shortcuts import render
from .models import Event, Ticket
from apps.accounts.models import UserProfile 
from django.views import View


# Create your views here.
class EventView(View):
    def get(self, request, *args, **kwargs):
        # Получает путь из запроса и возвращает информацию о конкретном событии, которому соответствует этот путь
        slug_match = request.path[request.path.rfind("/") + 1 :]
        event = Event.objects.get(slug=slug_match)
        ticket = Ticket.objects.filter(event=event)
        user =  UserProfile.objects.get
        if event:
            return render(request, "events/index.html", context={"event": event, "ticket": ticket, "user": user})

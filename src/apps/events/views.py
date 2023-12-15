from django.shortcuts import render
from .models import Event, Ticket
from apps.buildings.models import Area
from apps.accounts.models import UserProfile
from django.views.generic import TemplateView
from django.views import View
from django.db.models import Q
import re


# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):
        popular_events = Event.objects.order_by('-people_count')
        event = Event.objects.all()
        profile = UserProfile.objects.all()
        ticket = Ticket.objects.all()
        return render(request, "events/index.html", context={"profile": profile, "popular_events": popular_events, "event": event, "ticket": ticket})


class EventView(View):
    def get(self, request, filter, *args, **kwargs):
        # Получает путь из запроса и возвращает информацию о конкретном событии, которому соответствует этот путь
        slug_match = request.path[request.path.rfind("/") + 1 :]
        event = Event.objects.get(slug=slug_match)
        ticket = Ticket.objects.get(event=event)
        area = Area.objects.get(name = event.place.name)
        with open("apps/events/static/main/schemas/Frame.svg") as f:
            svg = f.read()
        # Проверяем, что у пользователя есть профиль
        if hasattr(request.user, "profile"):
            profile = request.user.profile
        else:
            profile = None
        if event:

            return render(request, "events/event.html", context={"profile": profile, "event": event, "ticket": ticket,
                                                                 "area": area, "svg": svg})


class SportView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        ticket = Ticket.objects.all()
        return render(
            request, "events/sport.html", context={"event": event, "ticket": ticket}
        )


class ConcertsView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        ticket = Ticket.objects.all()
        return render(
            request, "events/concerts.html", context={"event": event, "ticket": ticket}
        )


class FestivalsView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        ticket = Ticket.objects.all()
        return render(
            request, "events/festivals.html", context={"event": event, "ticket": ticket}
        )


class KidsView(View):
    def get(self, request, *args, **kwargs):
        event = Event.objects.all()
        ticket = Ticket.objects.all()
        return render(
            request, "events/kids.html", context={"event": event, "ticket": ticket}
        )


class CoopView(TemplateView):
    template_name = "events/cooperation.html"


class AboutView(TemplateView):
    template_name = "events/about.html"


class BonusView(TemplateView):
    template_name = "events/bonus.html"

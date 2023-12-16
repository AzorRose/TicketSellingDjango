from django.shortcuts import render
from .models import Event, Ticket
from apps.buildings.models import Area, Building
from apps.accounts.models import UserProfile
from django.views.generic import TemplateView
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from apps.events.models import Booked_Places
from django.http import HttpResponse
from ast import literal_eval


# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):
        popular_events = Event.objects.order_by('-people_count')
        event = Event.objects.all()
        profile = UserProfile.objects.all()
        ticket = Ticket.objects.all()
        query = request.GET.get('q')
        if query:
            events = Event.objects.filter(
                Q(name__icontains=query) |  # Поиск по имени
                Q(description__icontains=query)  # Поиск по описанию (можете добавить другие поля)
            ).distinct()
        else:
            events = Event.objects.all()
        return render(request, "events/index.html", context={"profile": profile, "popular_events": popular_events, "ticket": ticket, "event": event})


class EventView(View):
    def get(self, request, filter, *args, **kwargs):
        # Получает путь из запроса и возвращает информацию о конкретном событии, которому соответствует этот путь
        slug_match = request.path[request.path.rfind("/") + 1 :]
        event = Event.objects.get(slug=slug_match)
        ticket = Ticket.objects.get(event=event)
        area = Area.objects.get(name = event.place.name)
        building = Building.objects.get(name=event.place)
        with open("apps/events/static/main/schemas/Frame.svg") as f:
            svg = f.read()
        # Проверяем, что у пользователя есть профиль
        if hasattr(request.user, "profile"):
            profile = request.user.profile
        else:
            profile = None
        if event:
            return render(request, "events/event.html", context={"profile": profile, "event": event, "ticket": ticket,
                                                                 "area": area, "building": building, "svg": svg})
    def post(self, request, *args, **kwargs):
        row = literal_eval(request.body.decode('utf-8'))
        print(f'Ряд: {row["key1"]}')
        print(f'Место: {row["key2"]}')
        return HttpResponse("Ok")
        
def get_booked_places(request):
    booked_places = list(Booked_Places.objects.values('spot_row', 'spot_num', 'available'))
    return JsonResponse({'booked_places': booked_places}, safe=False)

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        
        events = get_events(query) 
        
        for event in events:
            event.tickets = Ticket.objects.filter(event=event)
             
        return render(request, "events/search_results.html", context={'events': events, 'query': query})

def get_events(query):    
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | 
                                    Q(description__icontains=query)
                                    ).distinct()
    else:
        events = Event.objects.all()
        
    return events

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

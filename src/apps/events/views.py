import json
from django.shortcuts import get_object_or_404, render
from .models import Event, Ticket
from apps.buildings.models import Area
from apps.accounts.models import UserProfile, Purchase
from django.views.generic import TemplateView
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse


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
                Q(description__icontains=query)  # Поиск по описанию 
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
        with open("apps/events/static/main/schemas/Frame.svg") as f:
            svg = f.read()
        if hasattr(request.user, "profile"):
            profile = request.user.profile
        else:
            profile = None
        if event:
            return render(request, "events/event.html", context={"profile": profile, "event": event, "ticket": ticket,
                                                                 "area": area, "svg": svg, "slug": slug_match, "filter": filter})
        
    def post(self, request, *args, **kwargs):
        slug_match = request.path[request.path.rfind("/") + 1 :]
        event = Event.objects.get(slug=slug_match)
        profile = request.user.profile
        data = json.loads(request.body.decode('utf-8'))
        selected_seats = data.get('selectedSeats', {})
         # Пройдемся по данным о выбранных местах и создадим покупку для каждого места
        for key, value in selected_seats.items():
                
                spot_row = value.get('row')
                spot_num = value.get('seat')
                spot_type = value.get("type")
                # Попробуем получить объект Booked_Places по данным о месте
                booked_places = event.booked_places
                            
                place = booked_places["items"][spot_type][spot_row][spot_num]
                ticket = Ticket.objects.get(id=place["ticket"])
                if place["available"]:
                    #Если место доступно, создадим покупку
                   new_purchase = Purchase(user=profile, ticket=ticket, spot_num=spot_num, spot_row=spot_row)
                   new_purchase.save()
                    
        response_data = {'message': 'OK'}
        return JsonResponse(response_data)

def get_booked_places(request, filter, slug):
    if not slug:
        return JsonResponse({"error": "Slug not provided"}, status=400)
    event = get_object_or_404(Event, slug=slug)
    
    # массив с местами    
    seats = event.booked_places
    
    transformed_data = []

    for spot_row, row_data in seats["items"]['seat'].items():
        for spot_num, seat_data in row_data.items():
            transformed_seat = {
                "spot_row": int(spot_row),
                "spot_num": int(spot_num),
                "available": seat_data['available']
            }
            transformed_data.append(transformed_seat)

    return JsonResponse({"booked_places": transformed_data}, safe=False)



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

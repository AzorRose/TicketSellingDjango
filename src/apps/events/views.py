from django.shortcuts import render
from .models import Event
from django.views import View
from re import findall

# Create your views here.
class EventView(View):
    def get(self, request, *args, **kwargs):
        path = request.path
        slug_match = path[path.rfind('/')+1:]
        event = Event.objects.filter(slug=slug_match)
        return render(request, "events/index.html", context={"event": event})

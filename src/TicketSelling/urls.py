"""
URL configuration for TicketSelling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView as logout_view
from apps.accounts.views import SignUpView, SignInView, ProfileView, AddBalanceView
from apps.events.views import EventView, MainView, SportView, ConcertsView, FestivalsView, KidsView, CoopView, AboutView, BonusView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", MainView.as_view(), name="index"),
    path("logout", logout_view.as_view(), name="logout"),
    path("<str:filter>/<slug:slug>", EventView.as_view(), name="events"),
    path("sport", SportView.as_view(), name="sport"),
    path("concerts", ConcertsView.as_view(), name="concerts"),
    path("festivals", FestivalsView.as_view(), name="festivals"),
    path("kids", KidsView.as_view(), name="kids"),
    path("cooperation", CoopView.as_view(), name="cooperation"),
    path("about", AboutView.as_view(), name="about"),
    path("bonus", BonusView.as_view(), name="bonus"),
    path("add_balance", AddBalanceView.as_view(), name="add_balance"),
]

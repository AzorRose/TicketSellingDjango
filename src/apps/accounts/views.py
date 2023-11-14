from django.shortcuts import render
from django.views import View
from .models import UserProfile
from .forms import SigUpForm, SignInForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError


# Create your views here.
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(
            request,
            "accounts/signup.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError as e:
                e = "This username already taken!"
                return render(
                    request, "accounts/signup.html", context={"form": form, "e": e}
                )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
        return render(
            request,
            "accounts/signup.html",
            context={
                "form": form,
            },
        )


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(
            request,
            "accounts/signin.html",
            context={
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
        return render(
            request,
            "accounts/signin.html",
            context={
                "form": form,
            },
        )


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        context["first_name"] = self.request.user.profile.first_name
        context["second_name"] = self.request.user.profile.second_name
        context["balance"] = self.request.user.profile.balance
        return context

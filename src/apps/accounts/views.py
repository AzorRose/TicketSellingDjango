from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from apps.events.models import Ticket
from .forms import SigUpForm, SignInForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from .models import Purchase


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
        user = self.request.user
        purchases = Purchase.objects.filter(user=user.profile)
        context["purchases"] = purchases
        context["username"] = user.username
        context["first_name"] = user.profile.first_name
        context["second_name"] = user.profile.second_name
        context["balance"] = user.profile.balance
        context["bonus"] = user.profile.bonus
        context["buyback_sum"] = user.profile.buyback_sum
        
        return context


class AddBalanceView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "profile"):
            profile = user.profile
            balance_input = request.POST.get("balance_input")
            if balance_input and balance_input.isdigit():
                profile.add_balance(int(balance_input))

        return redirect("profile")
    

class ShoppingCartView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        ticket = Ticket.objects.all()
        if hasattr(user, "profile"):
            profile = user.profile
            basket = profile.get_basket
            basket_sum = profile.basket_sum

        return render(
            request, "accounts/shopping_cart.html", context={"basket" : basket, "basket_sum": basket_sum, "ticket": ticket}
        )    

class BuyEventView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "profile"):
            # Получаем объект профиля
            profile = user.profile
            profile.buy()

        return redirect("profile")

class RemoveFromCartView(View):
    def post(self, request, purchase_id, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(id=purchase_id)
            purchase.delete()
        except Purchase.DoesNotExist:
            # Обработка случая, когда покупка не найдена
            pass
        return redirect("cart")
    
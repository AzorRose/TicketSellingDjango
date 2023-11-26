from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class SigUpForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Логин"}),
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Имя"}),
    )

    second_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "Фамилия"}),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Придумайте пароль"}
        ),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Повторите пароль"}
        ),
    )

    birth_date = forms.DateField(
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
    )

    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
    ]

    gender = forms.ChoiceField(
        label="Пол",
        widget=forms.RadioSelect(attrs={"class": "radio_input", "type": "radio"}),
        choices=GENDER_CHOICES,
    )

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["repeat_password"]

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],

            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["second_name"],

        )

        user_profile = UserProfile.objects.create(
            user=user,
            first_name=self.cleaned_data["first_name"],
            second_name=self.cleaned_data["second_name"],
            gender=self.cleaned_data["gender"],
            birth_date=self.cleaned_data["birth_date"],
            balance=0,
            bonus=0,
            buyback_sum=0,
        )

        auth = authenticate(**self.cleaned_data)

        return auth


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "alexsey@gmail.com"}
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Введите пароль"}
        ),
    )

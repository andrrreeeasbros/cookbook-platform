from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post_recipe, Reviews, UserProfile
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings


class UserRegistration(UserCreationForm):
    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'password1', 'password2', 'email']

    def check_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Отправка письма после сохранения пользователя
            self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        subject = 'Добро пожаловать на наш сайт!'
        message = f'Привет, {
            user.username}! Спасибо за регистрацию на нашем сайте.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)


class CustomAuthenticationForm(AuthenticationForm):
    pass


# TODO: Форма регистрации и аутентификации пользователей(Регистрация нового пользователя, Вход в систему, Сброс пароля и изменение пароля)
# TODO: Форма создания нового рецепта
# TODO: Форма редактирования рецепта
# TODO: Форма добавления отзыва
# TODO: Форма поиска и фильтрации рецептов
# TODO: Форма личного профиля пользователя
# TODO: Форма загрузки и редактирования фото для рецепта
# TODO: Форма контактной обратной связи

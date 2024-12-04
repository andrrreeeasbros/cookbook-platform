from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from profanity import profanity


class UserRegistration(UserCreationForm):
    username = forms.CharField(max_length=20, required=True,
                               label='Имя пользователя', help_text="Введите имя пользователя")
    name = forms.CharField(max_length=20, required=True,
                           label='Ваше имя', help_text="Введите ваше имя")
    email = forms.EmailField(required=True, label="Email",
                             help_text="Введите ваш email")

    class Meta:
        model = User
        fields = ['username', 'name', 'password1', 'password2', 'email']

    # Валидация для поля username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Имя пользователя не может быть пустым.')

        special_characters = [
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';',
            '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '}', '|', '~',
            '¥', '€', '©', '®', '°', '§', '¶', '≠', '±'
        ]
        if any(char in special_characters for char in username):
            raise ValidationError(
                'Имя пользователя не может содержать специальные символы.')

        # Проверка на матерные слова
        if profanity.contains_profanity(username):
            raise ValidationError(
                'Имя пользователя не может содержать матерные слова.')

        return username

    # Валидация для поля password2
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Это имя пользователя уже занято.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже зарегистрирован.')
        return email

    # Сохранение пользователя и отправка email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']  # Сохраняем имя пользователя
        if commit:
            user.save()  # Сохраняем пользователя в БД

            self.send_confirmation_email(user)

        return user

    # Функция отправки письма

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

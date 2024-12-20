from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from profanity import profanity
from django.db import IntegrityError
from .models import Post_recipe

class PostRecipeForm(forms.ModelForm):
    class Meta:
        model = Post_recipe
        fields = [
            'name', 
            'categories', 
            'cuisines', 
            'level', 
            'ingredients_list', 
            'steps', 
            'cooking_time', 
            'dish_photo'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple,  
            'cuisines': forms.CheckboxSelectMultiple,    
            'steps': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  
        }

    def clean_ingredients_list(self):
        ingredients = self.cleaned_data.get('ingredients_list')
        if profanity.contains_profanity(ingredients):
            raise forms.ValidationError("Ingredients list contains inappropriate words.")
        return ingredients

    def clean_steps(self):
        steps = self.cleaned_data.get('steps')
        if profanity.contains_profanity(steps):
            raise forms.ValidationError("Steps contains inappropriate words.")
        return steps








# TODO: Форма регистрации и аутентификации пользователей(Регистрация нового пользователя, Вход в систему, Сброс пароля и изменение пароля)
# TODO: Форма создания нового рецепта
# TODO: Форма редактирования рецепта
# TODO: Форма добавления отзыва
# TODO: Форма поиска и фильтрации рецептов
# TODO: Форма личного профиля пользователя
# TODO: Форма загрузки и редактирования фото для рецепта
# TODO: Форма контактной обратной связи

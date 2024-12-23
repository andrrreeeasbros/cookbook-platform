from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *


app_name = 'RecipeHub'


urlpatterns = [
    path('', main_template, name='main_template'),
    path('Категории рецептов/', categories, name='categories'),
    path('Лучшие рецепты/', best_recipes, name='best_recipes'),
    path('Рецепты/', create_post_recipe_and_list, name='recipes'),
    path('Отзывы/', reviews, name='reviews'),
    path('Рецепты/<str:name>/', recipe_details, name='recipe_detail'),
    path('Категории рецептов/Мировая кухня/<int:pk>/',
         cuisine_detail, name='cuisine_detail'),
    path('recipe-details/<str:name>/', recipe_details, name='recipe-details'),
    path('Профиль/', profile, name='profile'),
    path('Категории рецептов/<str:category_name>/',
         category_recipes, name='category_recipes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

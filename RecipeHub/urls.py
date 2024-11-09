from django.urls import path
from RecipeHub.views import *

app_name = 'RecipeHub'

urlpatterns = [
    path('', main_template, name='main_template'),
    path('categories/', categories, name='categories'),
    path('about_us/', about_us, name='about_us'),
    path('popular_recipes/', best_recipes, name='best_recipes'),
    path('recipes/', recipes, name='recipes'),
    path('reviews/', reviews, name='reviews'),
    path('contacts/', contacts, name='contacts'),
    path('recipe/<str:name>/', recipe_details, name='recipe_details'),
]

from django.urls import path
from RecipeHub.views import *

app_name = 'RecipeHub'

urlpatterns = [
    path('', main_template, name='main_template'),
    path('categories/', categories, name='categories'),
    path('about_us/', about_us, name='about_us'),
    path('best_recipes/', best_recipes, name='best_recipes'),
    path('recipes/', recipes, name='recipes'),
    path('reviews/', reviews, name='reviews'),
    path('contacts/', contacts, name='contacts'),
    path('recipe/<str:name>/', recipe_details, name='recipe_detail'),
    path('best_recipes/<str:name>/', best_recipe_details, name='best_recipe_detail')
]

from django.urls import path
from RecipeHub.views import *

app_name = 'RecipeHub'

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('recipe/<str:name>/', recipe_details, name='recipe_details'),
    path('categories/', categories, name='categories'),
    path('about_us/', about_us, name='about_us'),
    path('popular_recipes/', popular_recipes, name='popular_recipes'),
    path('recipes/', recipes, name='recipes'),
    path('reviews/', reviews, name='reviews'),
    path('contacts/', contacts, name='contacts'),
]


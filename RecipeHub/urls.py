from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *


app_name = 'RecipeHub'

urlpatterns = [
    path('', main_template, name='main_template'), 
    path('profile/', profile, name='profile'),
    path('categories/', categories, name='categories'),
    path('about_us/', about_us, name='about_us'),
    path('best_recipes/', best_recipes, name='best_recipes'),
    path('recipes/', recipes, name='recipes'),
    path('reviews/', reviews, name='reviews'),
    path('contacts/', contacts, name='contacts'),
    path('recipe/<str:name>/', recipe_details, name='recipe_detail'),
    path('categories/kitchens/', world_kitchens,name='world_kitchens'),
    path('categories/kitchens/<int:pk>/', cuisine_detail, name='cuisine_detail'),
    path('recipe-details/<str:name>/', recipe_details, name='recipe-details'),
    path('vegetarian/', vegetarian_recipes, name='vegetarian_recipes'),
    path('quick/', quick_recipes, name='quick_recipes'),
    path('dessert/', dessert_recipes, name='dessert_recipes'),
    path('vegan/', vegan_recipes, name='vegan_recipes'),
    path('drink/', drink_recipes, name='drink_recipes'),
    path('snacks/', snack_recipes, name='snack_recipes'),
    path('side-dishes/', side_dish_recipes, name='side_dish_recipes'),
    path('baking/', baking_recipes, name='baking_recipes'),
    path('register/', registration, name='registration'), 
    path('login/', login, name='authorization'),
    path('logout/', logout, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

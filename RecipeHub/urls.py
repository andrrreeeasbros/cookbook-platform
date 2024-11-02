from django.urls import path
from RecipeHub import views

app_name = 'RecipeHub'

urlpatterns = [
    path('',views.recipe_list, name='recipe_list'),
    path('recipe/<str:name>/',views.recipe_details, name='recipe_details'),
    path('categorories/', views.categories, name='categories')
]


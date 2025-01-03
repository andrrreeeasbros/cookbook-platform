from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'RecipeHub'

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main_template'),
    path('Categories/', CategoriesView.as_view(), name='categories'),
    path('Best Recipes/', BestRecipesView.as_view(), name='best_recipes'),
    path('Recipes/', CreatePostRecipeAndListView.as_view(), name='recipes'),
    path('Reviews/', ReviewsView.as_view(), name='reviews'),
    path('Recipes/<str:name>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('Categories/Cuisine/<int:pk>/', CuisineDetailView.as_view(), name='cuisine_detail'),
    path('recipe-details/<str:name>/', RecipeDetailView.as_view(), name='recipe-details'),
    path('Profile/', ProfileView.as_view(), name='profile'),
    path('Categories/<str:category_name>/', CategoryRecipesView.as_view(), name='category_recipes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe
from django.http import Http404


# представление для всех рецептов
def recipe_list(request):
    recipes = Post_recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})

# представление для одного рецепта
def recipe_details(request, name):
    recipe = get_object_or_404(Post_recipe.recipe_manager, name=name)
    return render(request, 'recipes/recipe_detail.html', {'recipe':recipe})


def categories(request):
    return render(request, 'menu/categories.html')


def about_us(request):
    return render(request, 'menu/about_us.html')


def popular_recipes(request):
    return render(request, 'menu/popular_recipes.html')


def recipes(request):
    return render(request, 'menu/recipes.html')


def reviews(request):
    return render(request, 'menu/reviews.html')

def contacts(request):
    return render(request, 'menu/contacts.html')
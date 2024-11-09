from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.http import Http404


def main_template(request):
    return render(request, 'index.html')


def categories(request):
    return render(request, 'menu/categories.html')


def about_us(request):
    return render(request, 'menu/about_us.html')


def best_recipes(request):
    best_reviews = Reviews.review_manager.all()
    best_recipes = set()
    for review in best_reviews:
        best_recipes.add(review.recipe)
    return render(request, 'menu/best_recipes.html', {'best_recipes': best_recipes})


def reviews(request):
    reviews = Reviews.objects.all()
    return render(request, 'menu/reviews.html', {'reviews': reviews})


def contacts(request):
    return render(request, 'menu/contacts.html')


def recipes(request):
    recipes = Post_recipe.objects.all()  # представление для всех рецептов
    return render(request, 'menu/recipes.html', {'recipes': recipes})


def recipe_details(request, name):  # представление для одного рецепта
    recipe = get_object_or_404(Post_recipe.recipe_manager, name=name)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

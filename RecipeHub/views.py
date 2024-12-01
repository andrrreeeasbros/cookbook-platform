from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .forms import UserRegistration
from django.contrib.auth import login
from django.contrib import messages

def main_template(request):  # представдение для главного шаблона сайта
    return render(request,
                  'index.html')
    

def profile(request):
    return render(request, 'menu/profile.html')


def categories(request):  # представдение категорий рецептов
    return render(request,
                  'menu/categories.html')


def about_us(request):  # представление об авторе сайта
    return render(request,
                  'menu/about_us.html')


def best_recipes(request):  # представление для лучших рецептов
    best_reviews = Reviews.review_manager.all()
    best_recipes = []
    for review in best_reviews:
        if review.recipe not in best_recipes:
            best_recipes.append(review.recipe)
    paginator = Paginator(best_recipes, 2)
    page_number = request.GET.get('best_recipes', 1)
    try:
        recipes_pages = paginator.get_page(page_number)
    except EmptyPage:
        recipes_pages = paginator.get_page(1)
        
    return render(request,
                  'menu/best_recipes.html',
                  {'best_recipes': recipes_pages})


def contacts(request):  # представление для связи с разработчиком
    return render(request,
                  'menu/contacts.html')


def recipes(request):
    recipes = Post_recipe.objects.all()  # представление для всех рецептов
    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page')
    try:
        recipes_page = paginator.get_page(page_number)
    except EmptyPage:
        recipes_page = paginator.get_page(1)
    return render(request,
                  'menu/recipes.html',
                  {'recipes': recipes_page})


def reviews(request):
    reviews = Reviews.objects.all()  # представление для всех отзывов
    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('review', 1)
    try:
        reviews_page = paginator.get_page(page_number)
    except EmptyPage:
        reviews_page = paginator.get_page(1)
    return render(request,
                  'menu/reviews.html',
                  {'reviews': reviews_page})


def recipe_details(request, name):  # представление для одного рецепта
    try:
        recipe = Post_recipe.objects.get(name=name)
    except Post_recipe.DoesNotExist:
        raise Http404("Рецепт не найден")
    return render(request,
                  'details/recipe_details.html',
                  {'recipe': recipe})


def best_recipe_details(request, name):
    try:
        best_recipe = Post_recipe.objects.get(name=name)
    except Post_recipe.DoesNotExist:
        raise Http404("Рецепт не найден")
    return render(request,
                  'details/best_recipe_details.html',
                  {'best_recipe': best_recipe})

def Registration(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        
        if form.is_valid():
            # Сохраняем нового пользователя
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
        else:
            # Если форма не валидна, покажем ошибки
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegistration()

    return render(request, 'user/registration.html', {'form': form})

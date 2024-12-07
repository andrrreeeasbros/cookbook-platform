from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .forms import UserRegistration, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse


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


def best_recipes(request):  
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
    
def recipe_details(request, name):
    try:
        recipe = Post_recipe.objects.get(name=name)  
    except Post_recipe.DoesNotExist:
        return JsonResponse({'error': 'Рецепт не найден'}, status=404)
    
    ingredients_list = recipe.ingredients_list.splitlines()
    steps_list = recipe.steps.splitlines()
    
    data = {
        'name': recipe.name,
        'categories': recipe.categories,
        'world_cuisine_categories': recipe.world_cuisine_categories,
        'meal_time': recipe.meal_time,
        'level': recipe.level,
        'ingredients': ingredients_list,
        'steps': steps_list,
        'cooking_time': recipe.cooking_time,
        'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,  
    }
    
    return JsonResponse(data)


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


def registration(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        
        if form.is_valid():
            login(request, form.save())
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('RecipeHub:authorization')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            form = UserRegistration()
            
    return render(request, 'user/registration.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        
    if form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Вы успешно вошли!')
        return redirect('RecipeHub:main_template')
    else:
        messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        form = CustomAuthenticationForm()
    
    return render(request, 'user/authorization.html')

def logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('RecipeHub:main_template')
        
    
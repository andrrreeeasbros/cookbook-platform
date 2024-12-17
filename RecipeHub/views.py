from django.db.models import Avg
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.core.paginator import Paginator, EmptyPage
from .forms import UserRegistration, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from RecipeHub.models import Cuisine
from RecipeHub.models import Category
from .forms import PostRecipeForm
from .models import UserProfile
from django.urls import reverse_lazy
from .models import UserProfile
from django.contrib.auth.models import User

def main_template(request):
    return render(request,
                  'index.html')

def about_us(request):
    return render(request,
                  'menu/about_us.html')


def categories(request):
    categories = Category.objects.all()
    return render(request,
                  'menu/categories.html', {'categories': categories})


def best_recipes(request):
    best_recipes = Post_recipe.objects.annotate(
        avg_rating=Avg('reviews__grade__value')
    ).filter(avg_rating__gt=4)

    paginator = Paginator(best_recipes, 10)
    page_number = request.GET.get('page', 1)
    try:
        recipes_pages = paginator.get_page(page_number)
    except EmptyPage:
        recipes_pages = paginator.get_page(1)

    return render(request, 'menu/best_recipes.html', {'best_recipes': recipes_pages})


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

    # Serialize the related categories (assuming 'categories' is a Many-to-Many relationship)
    categories_list = [category.name for category in recipe.categories.all()]

    data = {
        'name': recipe.name,
        'categories': categories_list,
        'level': recipe.level.name if recipe.level else None,  # If no level, set as None
        'ingredients': ingredients_list,
        'steps': steps_list,
        'cooking_time': recipe.minutes_to_hours_to_days(),
        'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,
    }

    return JsonResponse(data)

def add_recipe(request):
    if request.method == 'POST':
        form = PostRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Рецепт успешно добавлен!'})
        else:
            # Отправляем ошибки формы обратно
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = PostRecipeForm()
    
    return render(request, 'your_template_name.html', {'form': form})



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


def vegetarian_recipes(request):
    recipes = Post_recipe.vegetarian_manager.all()
    return render(request, 'categories/vegetarian_recipes.html', {'recipes': recipes, 'category': 'Вегетарианские блюда'})


def quick_recipes(request):
    recipes = Post_recipe.quick_manager.all()  
    return render(request, 'categories/quick_recipes.html', {'recipes': recipes, 'category': 'Еда быстрого приготовления'})


def dessert_recipes(request):
    recipes = Post_recipe.dessert_manager.all()  
    return render(request, 'categories/dessert_recipes.html', {'recipes': recipes, 'category': 'Десерты'})


def vegan_recipes(request):
    recipes = Post_recipe.vegan_manager.all()  # Все веганские рецепты
    return render(request, 'categories/vegan_recipes.html', {'recipes': recipes, 'category': 'Веганские блюда'})


def drink_recipes(request):
    recipes = Post_recipe.drink_manager.all()  # Все напитки
    return render(request, 'categories/drink_recipes.html', {'recipes': recipes, 'category': 'Напитки'})


def snack_recipes(request):
    recipes = Post_recipe.snack_manager.all()  # Все закуски
    return render(request, 'categories/snack_recipes.html', {'recipes': recipes, 'category': 'Закуски'})


def side_dish_recipes(request):
    recipes = Post_recipe.side_dish_manager.all()  # Все гарниры
    return render(request, 'categories/side_dish_recipes.html', {'recipes': recipes, 'category': 'Гарниры'})


def baking_recipes(request):
    recipes = Post_recipe.baking_manager.all()  # Все печенье и выпечка
    return render(request, 'categories/baking_recipes.html', {'recipes': recipes, 'category': 'Печенье и выпечка'})


def world_kitchens(request):
    cuisines = Cuisine.objects.all()
    return render(request, 'categories/world_kitchen_list.html', {'cuisines': cuisines})


def cuisine_detail(request, pk, cuisine_name=None):

    cuisine = get_object_or_404(Cuisine, pk=pk)
    if cuisine_name:
        recipes = Post_recipe.objects.filter(cuisines=cuisine)

        # Добавим дополнительную фильтрацию, если выбран менеджер кухни
        if cuisine_name == "Итальянская":
            recipes = recipes.filter(cuisines__name="Итальянская")
        elif cuisine_name == "Французская":
            recipes = recipes.filter(cuisines__name="Французская")
        elif cuisine_name == "Японская":
            recipes = recipes.filter(cuisines__name="Японская")
        elif cuisine_name == "Китайская":
            recipes = recipes.filter(cuisines__name="Китайская")
        elif cuisine_name == "Мексиканская":
            recipes = recipes.filter(cuisines__name="Мексиканская")
        elif cuisine_name == "Тайская":
            recipes = recipes.filter(cuisines__name="Тайская")
        elif cuisine_name == "Индийская":
            recipes = recipes.filter(cuisines__name="Индийская")
        elif cuisine_name == "Греческая":
            recipes = recipes.filter(cuisines__name="Греческая")
        elif cuisine_name == "Испанская":
            recipes = recipes.filter(cuisines__name="Испанская")
        else:
            recipes = recipes.all()
    else:

        recipes = Post_recipe.objects.filter(cuisines=cuisine)

    return render(request, 'categories/cuisine_detail.html', {'cuisine': cuisine, 'recipes': recipes})

def profile(request):
    # Assuming you want to display the profile for the logged-in user
    try:
        profile = UserProfile.profiles.get(user=request.user)  # Retrieve the profile for the logged-in user
    except UserProfile.DoesNotExist:
        profile = None  # If no profile exists for the user, display None

    # Passing the profile data to the template
    return render(request, 'menu/profile.html', {'profile': profile})


def set_user_default():
    default_user = User.objects.first()  
    return default_user
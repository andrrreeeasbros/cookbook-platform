from django.db.models import Avg
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .forms import UserRegistration, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from RecipeHub.models import Cuisine
from RecipeHub.models import Category


def main_template(request):
    return render(request,
                  'index.html')


def profile(request):
    return render(request, 'menu/profile.html')


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


def recipe_detail(request, recipe_name):
    recipe = Post_recipe.objects.get(name=recipe_name)
    return render(request, 'Recipehub/recipe_detail.html', {'recipe': recipe})


def vegetarian_recipes(request):
    recipes = Post_recipe.vegetarian_recipes.all()
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Вегетарианские блюда'})


def quick_recipes(request):
    recipes = Post_recipe.quick_recipes.all()  # Все рецепты быстрого приготовления
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Еда быстрого приготовления'})


def dessert_recipes(request):
    recipes = Post_recipe.dessert_recipes.all()  # Все десерты
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Десерты'})


def vegan_recipes(request):
    recipes = Post_recipe.vegan_recipes.all()  # Все веганские рецепты
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Веганские блюда'})


def drink_recipes(request):
    recipes = Post_recipe.drink_recipes.all()  # Все напитки
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Напитки'})


def snack_recipes(request):
    recipes = Post_recipe.snack_recipes.all()  # Все закуски
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Закуски'})


def side_dish_recipes(request):
    recipes = Post_recipe.side_dish_recipes.all()  # Все гарниры
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Гарниры'})


def baking_recipes(request):
    recipes = Post_recipe.baking_recipes.all()  # Все печенье и выпечка
    return render(request, 'Recipehub/category_recipes.html', {'recipes': recipes, 'category': 'Печенье и выпечка'})


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

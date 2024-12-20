from django.db.models import Avg
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe, Reviews
from django.core.paginator import Paginator, EmptyPage
from .forms import UserRegistration, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from RecipeHub.models import Cuisine
from RecipeHub.models import Category
from .forms import PostRecipeForm
from .models import UserProfile
from django.urls import reverse_lazy
from .models import UserProfile


def main_template(request):
    return render(request,
                  'index.html')


def categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 9)
    page_number = request.GET.get('page')
    try:
        categories_pages = paginator.get_page(page_number)
    except:
        categories_pages = paginator.get_page(1)
        
    return render(request,
                  'menu/categories.html', {'categories': categories_pages})


def contacts(request):
    return render(request,
                  'menu/contacts.html')


def profile(request):
    try:
        profile = UserProfile.profiles.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'menu/profile.html', {'profile': profile})


def best_recipes(request):
    best_recipes = Post_recipe.objects.annotate(
        avg_rating=Avg('reviews__grade__value')
    ).filter(avg_rating__gt=4)

    paginator = Paginator(best_recipes, 1)
    page_number = request.GET.get('page', 1)
    try:
        recipes_pages = paginator.get_page(page_number)
    except EmptyPage:
        recipes_pages = paginator.get_page(1)

    return render(request, 'menu/best_recipes.html', {'best_recipes': recipes_pages})


def recipes_list(request):
    recipes = Post_recipe.objects.all()  
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

    if not recipe.steps:
        return JsonResponse({'error': 'Шаги приготовления не указаны'}, status=400)

    ingredients_list = recipe.ingredients_list.splitlines(
    ) if recipe.ingredients_list else []
    steps_list = recipe.steps.splitlines() if recipe.steps else []

    categories_list = [category.name for category in recipe.categories.all()]

    steps_data = []
    for idx, step in enumerate(steps_list, start=1):
        steps_data.append({
            'step_number': idx,
            'step_description': step
        })

    data = {
        'name': recipe.name,
        'categories': categories_list,
        # Если нет уровня, возвращаем None
        'level': recipe.level.name if recipe.level else None,
        'ingredients': ingredients_list,
        'steps': steps_data,  # Отправляем обработанные шаги
        'cooking_time': recipe.minutes_to_hours_to_days(),
        'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,
    }

    # Отладочная печать (для проверки данных)
    print("Steps Data:", steps_data)

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


def category_recipes(request, category_name):
    category_display_name = {
        'vegetarian': 'Вегетарианское',
        'quick-food': 'Еда быстрого приготовления',
        'desserts': 'Десерты',
        'vegan': 'Веганские блюда',
        'drinks': 'Напитки',
        'snacks': 'Закуски',
        'side-dishes': 'Гарниры',
        'baking': 'Печенье и выпечка',
    }

    display_name = category_display_name.get(
        category_name, category_name.capitalize())

    recipe_manager = Post_recipe.objects
    recipes = recipe_manager.filter_by_category(category_name)

    # Если категория "Мировая кухня"
    if category_name == "Мировая кухня":
        cuisines = Cuisine.objects.all()
        paginator = Paginator(cuisines , 9)
        page_number = request.GET.get("page", 1)
        try:
            cuisine_pages = paginator.get_page(page_number)
        except EmptyPage:
            cuisine_pages = paginator.get_page(1)
        
        return render(request, 'categories/world_kitchens_list.html', {'cuisines': cuisine_pages})

    return render(request, 'categories/categories_list.html', {
        'recipes': recipes,
        'category': display_name
    })


def cuisine_detail(request, pk, cuisine_name=None):
    cuisine = get_object_or_404(Cuisine, pk=pk)

    # Если cuisine_name передан, фильтруем рецепты
    if cuisine_name:
        cuisine_names = {
            "Итальянская": "Итальянская",
            "Французская": "Французская",
            "Японская": "Японская",
            "Китайская": "Китайская",
            "Мексиканская": "Мексиканская",
            "Тайская": "Тайская",
            "Индийская": "Индийская",
            "Греческая": "Греческая",
            "Испанская": "Испанская"
        }

        if cuisine_name in cuisine_names:
            recipes = Post_recipe.objects.filter(
                cuisines__name=cuisine_names[cuisine_name])
        else:
            recipes = Post_recipe.objects.filter(cuisines=cuisine)
    else:

        recipes = Post_recipe.objects.filter(cuisines=cuisine)

    return render(request, 'categories/cuisine_details.html', {'cuisine': cuisine, 'recipes': recipes})


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

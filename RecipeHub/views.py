from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from .models import Post_recipe, Reviews, Cuisine, Category, UserProfile
from .forms import PostRecipeForm, PostReviewForm
from django.contrib import messages


class MainTemplateView(TemplateView):
    template_name = 'index.html'


class CategoriesView(ListView):
    model = Category
    template_name = 'menu/categories.html'
    context_object_name = 'categories'
    paginate_by = 9

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        try:
            categories_page = paginator.get_page(page_number)
        except EmptyPage:
            categories_page = paginator.get_page(1)
        context['categories'] = categories_page
        return context


class CreatePostRecipeAndListView(View):
    @staticmethod
    def get_paginated_recipes(request):
        recipes = Post_recipe.objects.all()
        paginator = Paginator(recipes, 2)
        page_number = request.GET.get('page')
        try:
            recipes_page = paginator.get_page(page_number)
        except EmptyPage:
            recipes_page = paginator.get_page(1)
        return recipes_page

    def get(self, request):
        form = PostRecipeForm()
        recipes_page = self.get_paginated_recipes(request)
        return render(request, 'menu/recipes.html', {'form': form, 'recipes': recipes_page})

    def post(self, request):
        form = PostRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Рецепт успешно добавлен!")
            return redirect('RecipeHub:recipes')
        recipes_page = self.get_paginated_recipes(request)
        return render(request, 'menu/recipes.html', {'form': form, 'recipes': recipes_page})


class ProfileView(View):
    @staticmethod
    def get(request):
        profile = None
        if request.user.is_authenticated:
            try:
                profile = UserProfile.profiles.get(user=request.user)
            except UserProfile.DoesNotExist:
                profile = None
        return render(request, 'menu/profile.html', {'profile': profile})


class BestRecipesView(ListView):
    model = Post_recipe
    template_name = 'menu/best_recipes.html'
    context_object_name = 'best_recipes'
    paginate_by = 2

    def get_queryset(self):
        recipes = Post_recipe.objects.annotate(
            avg_rating=Avg('reviews__grade__value')
        ).filter(avg_rating__gt=4)

        for recipe in recipes:
            recipe.formatted_cooking_time = format_duration(recipe.cooking_time)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        try:
            recipes_page = paginator.get_page(page_number)
        except EmptyPage:
            recipes_page = paginator.get_page(1)
        context['best_recipes'] = recipes_page
        return context


def format_duration(duration):
    days = duration.days
    seconds = duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} дн.")
    if hours > 0:
        parts.append(f"{hours} ч.")
    if minutes > 0:
        parts.append(f"{minutes} мин.")
    if seconds > 0:
        parts.append(f"{seconds} сек.")

    return ' '.join(parts) if parts else '0 сек.'


class RecipeDetailView(View):
    @staticmethod
    def get(request, name):
        try:
            recipe = Post_recipe.objects.get(name=name)
        except Post_recipe.DoesNotExist:
            return JsonResponse({'error': 'Рецепт не найден'}, status=404)

        if not recipe.steps:
            return JsonResponse({'error': 'Шаги приготовления не указаны'}, status=400)

        ingredients_list = recipe.ingredients_list.splitlines() if recipe.ingredients_list else []
        steps_list = recipe.steps.splitlines() if recipe.steps else []

        categories_list = [category.name for category in recipe.categories.all()]

        steps_data = []
        for idx, step in enumerate(steps_list, start=1):
            steps_data.append({
                'step_number': idx,
                'step_description': step
            })

<<<<<<< HEAD
        formatted_cooking_time = format_duration(recipe.cooking_time)
=======
    data = {
        'name': recipe.name,
        'categories': categories_list,
        # Если нет уровня, возвращаем None
        'level': recipe.level.name if recipe.level else None,
        'ingredients': ingredients_list,
        'steps': steps_data,  # Отправляем обработанные шаги
        'cooking_time': recipe.minutes_to_hours_to_days(),
        'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,  
        'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,
<<<<<<< HEAD
    
=======
    }
>>>>>>> c6cce7d5e1361f52a983e823b927c5b9c05d7998

        data = {
            'name': recipe.name,
            'categories': categories_list,
            'level': recipe.level.name if recipe.level else None,
            'ingredients': ingredients_list,
            'steps': steps_data,
            'cooking_time': formatted_cooking_time,
            'dish_photo': recipe.dish_photo.url if recipe.dish_photo else None,
        }

<<<<<<< HEAD
        return JsonResponse(data)
=======
>>>>>>> line
    return JsonResponse(data)
>>>>>>> c6cce7d5e1361f52a983e823b927c5b9c05d7998


class ReviewsView(View):
    @staticmethod
    def get(request):
        reviews = Reviews.objects.all()
        paginator = Paginator(reviews, 3)
        page_number = request.GET.get('review', 1)
        try:
            reviews_page = paginator.get_page(page_number)
        except EmptyPage:
            reviews_page = paginator.get_page(1)

        form = PostReviewForm()
        return render(request, 'menu/reviews.html', {'reviews': reviews_page, 'form': form})

    @staticmethod
    def post(request):
        form = PostReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('RecipeHub:reviews')


class CategoryRecipesView(View):
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

    def get(self, request, category_name):
        display_name = self.category_display_name.get(category_name, category_name.capitalize())

        if category_name == "Мировая кухня":
            cuisines = Cuisine.objects.all()
            paginator = Paginator(cuisines, 9)
            page_number = request.GET.get("page", 1)
            try:
                cuisine_pages = paginator.get_page(page_number)
            except EmptyPage:
                cuisine_pages = paginator.get_page(1)
            return render(request, 'categories/world_kitchens_list.html', {'cuisines': cuisine_pages})

        recipes = Post_recipe.objects.filter_by_category(category_name)
        return render(request, 'categories/categories_list.html', {'recipes': recipes, 'category': display_name})


class CuisineDetailView(View):
    @staticmethod
    def get(request, pk, cuisine_name=None):
        cuisine = get_object_or_404(Cuisine, pk=pk)

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
                recipes = Post_recipe.objects.filter(cuisines__name=cuisine_names[cuisine_name])
            else:
                recipes = Post_recipe.objects.filter(cuisines=cuisine)
        else:
            recipes = Post_recipe.objects.filter(cuisines=cuisine)

        return render(request, 'categories/cuisine_details.html', {'cuisine': cuisine, 'recipes': recipes})

from django.contrib import admin
from django.utils.html import format_html
from RecipeHub.models import Post_recipe, Reviews, UserProfile, Category, Cuisine, DifficultyLevel, Grade, Timezone, Age

# Регистрируем категории для админ панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'recipe_count')
    search_fields = ('name',)
    ordering = ('name',)

    def recipe_count(self, obj):
        return obj.recipes.count()
    recipe_count.short_description = 'Количество рецептов'


# Регистрируем кухни для админ панели
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


# Регистрируем уровни сложности для админ панели
@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# Регистрируем оценки для админ панели
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'value')
    search_fields = ('display_name',)
    ordering = ('value',)


# Регистрируем рецепты для админ панели
@admin.register(Post_recipe)
class PostRecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories', 'cuisines')  # Горизонтальные фильтры для категорий и кухонь
    list_display = ('name', 'get_categories', 'cooking_time', 'level', 'created_at', 'dish_photo_thumbnail')
    search_fields = ('name', 'ingredients_list', 'steps')
    list_filter = ('categories', 'cuisines', 'level')
    ordering = ('-created_at',)

    def get_categories(self, obj):
        categories = [category.name for category in obj.categories.all()]
        return ", ".join(categories)
    get_categories.short_description = 'Категории'

    def dish_photo_thumbnail(self, obj):
        if obj.dish_photo:
            return format_html('<img src="{0}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.dish_photo.url)
        return '-'
    dish_photo_thumbnail.short_description = 'Фото блюда'

    def minutes_to_hours_to_days(self, obj):
        return obj.minutes_to_hours_to_days()  # Используем метод модели для преобразования времени

    minutes_to_hours_to_days.short_description = 'Время приготовления'


# Регистрируем отзывы для админ панели
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe', 'grade', 'created_at', 'comments_preview')
    list_filter = ('grade', 'created_at')
    search_fields = ('author', 'comments')
    ordering = ('-created_at',)

    def comments_preview(self, obj):
        return f"{obj.comments[:50]}..."
    comments_preview.short_description = 'Комментарии'


# Регистрируем профили пользователей для админ панели
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'country', 'age', 'created_at', 'profile_photo_thumbnail')
    search_fields = ('name', 'description', 'user__username')
    ordering = ('-created_at',)

    def profile_photo_thumbnail(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{0}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.profile_photo.url)
        return '-'
    profile_photo_thumbnail.short_description = 'Фото профиля'


# Регистрируем Timezone для админ панели
@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('country', 'timezone')
    search_fields = ('country', 'timezone')
    ordering = ('country',)


# Регистрируем Age для админ панели
@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = ('years',)
    search_fields = ('years',)
    ordering = ('years',)

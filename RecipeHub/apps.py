from django.apps import AppConfig


class RecipehubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RecipeHub'

    def ready(self):
        from .models import Category
        Category.create_default_categories()
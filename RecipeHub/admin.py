from django.contrib import admin
from RecipeHub.models import Post_recipe

@admin.register(Post_recipe)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'cooking_time']
    search_fields = ['name', 'ingredients_list']
    list_filter = ['name', 'level']
    ordering = ['-created_at']




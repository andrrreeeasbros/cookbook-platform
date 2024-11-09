from django.contrib import admin
from RecipeHub.models import Post_recipe, Reviews


@admin.register(Post_recipe)
class PostRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass

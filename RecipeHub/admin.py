from django.contrib import admin
from RecipeHub.models import Post_recipe, Reviews, UserProfile


@admin.register(Post_recipe)
class PostRecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories','cuisines')
    
    list_display = ('name', 'get_categories')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Категории'
    
     
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


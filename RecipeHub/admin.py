from django.contrib import admin
from RecipeHub.models import Post_recipe, Reviews, UserProfile, Category


class PostRecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories', 'cuisines')
    
    list_display = ('name', 'get_categories')

    def get_categories(self, obj):
        # Исключаем категорию с именем "Мировая кухня"
        categories = [category.name for category in obj.categories.all() if category.name != "Мировая кухня"]
        return ", ".join(categories)
    
    get_categories.short_description = 'Категории'
    

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs['queryset'] = Category.objects.exclude(name="Мировая кухня")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Post_recipe, PostRecipeAdmin)

    
     
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from RecipeHub.models import Post_recipe
from django.http import Http404


# представление для всех рецептов
def recipe_list(request):
    recipes = Post_recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})
    
# представление для одного рецепта
def recipe_details(request, name):
    recipe = get_object_or_404(Post_recipe.recipe_manager, name=name)
    return render(request, 'recipes/recipe_detail.html', {'recipe':recipe})
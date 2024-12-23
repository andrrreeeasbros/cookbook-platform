from django import forms
from django.conf import settings
from .models import Post_recipe
from django import forms
from .models import Post_recipe



class PostRecipeForm(forms.ModelForm):
    class Meta:
        model = Post_recipe
        fields = ['name', 'categories', 'cuisines', 'level', 'ingredients_list', 'steps', 'cooking_time', 'dish_photo']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'cuisines': forms.CheckboxSelectMultiple(),
            'level': forms.Select(),
            'cooking_time': forms.NumberInput(attrs={'min': 1}),
            'dish_photo': forms.ClearableFileInput(), 
        }




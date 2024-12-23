from django import forms
from django.conf import settings
from profanity import profanity
from .models import Post_recipe, Grade
from django import forms
from profanity import profanity
from .models import Post_recipe, Category, Cuisine, DifficultyLevel


class PostRecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    cuisines = forms.ModelMultipleChoiceField(
        queryset=Cuisine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    level = forms.ModelChoiceField(
        queryset=DifficultyLevel.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = Post_recipe
        fields = ['name', 'categories', 'cuisines', 'level', 'ingredients_list', 'steps', 'cooking_time', 'dish_photo']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'cuisines': forms.CheckboxSelectMultiple(),
            'level': forms.Select(),
            'ingredients_list': forms.Textarea(attrs={'rows': 4}),
            'steps': forms.Textarea(attrs={'rows': 4}),
            'cooking_time': forms.NumberInput(attrs={'min': 1}),
        }




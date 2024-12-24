from .models import Reviews
from django import forms
from django.conf import settings
from .models import Post_recipe, Reviews


class PostRecipeForm(forms.ModelForm):
    class Meta:
        model = Post_recipe
        fields = ['name', 'categories', 'cuisines', 'level',
                  'ingredients_list', 'steps', 'cooking_time', 'dish_photo']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'cuisines': forms.CheckboxSelectMultiple(),
            'level': forms.Select(),
            'cooking_time': forms.NumberInput(attrs={'min': 1}),
            'dish_photo': forms.ClearableFileInput(),
        }


class PostReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['author', 'comments', 'grade', 'recipe']

    widgets = {
        'author': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
        'comments': forms.Textarea(attrs={'placeholder': 'Write your review here', 'class': 'form-control', 'rows': 4}),
        'grade': forms.Select(attrs={'class': 'form-control'}),
        'recipe': forms.Select(attrs={'class': 'form-control'}),
    }
    

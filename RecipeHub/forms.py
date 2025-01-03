from .models import Reviews
from django import forms
from .models import Post_recipe, Reviews, Category, Cuisine
from django.contrib.auth.forms import UserCreationForm


class PostRecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label="Категории"  
    )
    
    cuisines = forms.ModelMultipleChoiceField(
        queryset=Cuisine.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        label="Кухни"  
    )

    class Meta:
        model = Post_recipe
        fields = ['name', 'categories', 'cuisines', 'level',
                  'ingredients_list', 'steps', 'cooking_time', 'dish_photo']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={'min': 1}),
            'dish_photo': forms.ClearableFileInput(),
        }


class PostReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['author', 'recipe', 'grade', 'comments']

    widgets = {
        'author': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
        'comments': forms.Textarea(attrs={'placeholder': 'Write your review here', 'class': 'form-control', 'rows': 4}),
        'grade': forms.Select(attrs={'class': 'form-control'}),
        'recipe': forms.Select(attrs={'class': 'form-control'}),
    }

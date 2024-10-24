from django.db import models
from datetime import timedelta

# идеи для реализации полей и моделей
# модели для оставления пользователем комментария  
# поле рейтинга 
# поле кбжу ккал
# поле вегетерианское ли блюдо или мясное и тд

class Post_recipe(models.Model):
    

    DISH_LVL = (
        ('very_simple', 'Очень просто'),
        ('simple', 'Просто'),
        ('medium', 'Средней сложности'),
        ('hard', 'Сложно'),
        ('very_hard', 'Очень сложно'),
    )


    name = models.CharField(
        verbose_name='Название блюда', 
        primary_key=True,
        max_length=30, 
        unique=True,
        blank=False)
    
    ingredients_list = models.TextField(
        verbose_name='Ингридиенты данного рецепта',
        max_length=300,
        blank=False,
        help_text='Пожалуйста вводите каждый новый ингридиент с новой строки. Индексы проставяться сами')
    
    
    level = models.CharField(
        verbose_name='Уровень сложности',
        choices=DISH_LVL,
        max_length=20, 
        blank=False)
    
    steps = models.TextField(
        verbose_name='Шаги приготовления', 
        blank=False,
        help_text='Пожалуйста вводите каждый новый шаг с новой строки. Индексы проставяться сами')
    
    cooking_time = models.DurationField(
        verbose_name='Время приготовления блюда', 
        default=timedelta(minutes=30),
        help_text='Напишите примерное время приготовления данного блюда. По дефолту:30 min')
    
    dish_photo = models.ImageField(
        verbose_name='Фото блюда', 
        upload_to='dish_photos/', 
        blank=True, 
        null=True,
        help_text='Загрузите фото данного блюда.') # нужно к нему добавить валидаторы для конвертации картинки  
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания')
    
    
    def save(self, *args, **kwargs):
        if '\n' not in self.ingredients_list or '\n' not in self.steps:
            raise ValueError("Пожалуйста, вводите каждый ингредиент и шаг на новой строке.")
        
        self.ingredients_list = self.index_lines(self.ingredients_list)
        self.steps = self.index_lines(self.steps)
        super().save(*args, **kwargs)

    def index_lines(self, text):
        lines = text.strip().splitlines()
        indexed_lines = []
        current_index = 1
        
        for line in lines:
            if line and line[0].isdigit() and line[1] == '.':
                indexed_lines.append(line)
            elif line:
                indexed_lines.append(f"{current_index}. {line}")
                current_index += 1
        return "\n".join(indexed_lines)
    

    def formatted_ingredients(self):
        return self.ingredients_list

    def formatted_steps(self):
        return self.steps

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["-created_at"]



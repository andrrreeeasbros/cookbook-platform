from django.db import models
from datetime import timedelta
from django.urls import reverse
# идеи для реализации полей и моделей 
# поле кбжу ккал

class RecipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_vegetarian=True)


# 1. Модель - основная модель (рецептов и т.д.)
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
        blank=False
    )

    is_vegetarian = models.BooleanField(
        verbose_name='Вегетарианское ли блюдо?',
        default=False
    )

    level = models.CharField(
        verbose_name='Уровень сложности',
        choices=DISH_LVL,
        max_length=20,
        blank=False
    )

    ingredients_list = models.TextField(
        verbose_name='Ингредиенты данного рецепта',
        max_length=20000,
        blank=False,
        help_text='Пожалуйста, вводите каждый новый ингредиент с новой строки. Индексы проставятся сами.'
    )

    steps = models.TextField(
        verbose_name='Шаги приготовления',
        blank=False,
        help_text='Пожалуйста, вводите каждый новый шаг с новой строки. Индексы проставятся сами.'
    )

    cooking_time = models.DurationField(
        verbose_name='Время приготовления блюда',
        default=timedelta(minutes=30),
        help_text='Напишите примерное время приготовления данного блюда. По умолчанию: 30 мин.'
    )

    dish_photo = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='dish_photos/',
        blank=True,
        null=True,
        help_text='Загрузите фото данного блюда.'  # Нужно добавить валидаторы для конвертации картинки.
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

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

    objects = models.Manager()  # Менеджер, применяемый по умолчанию
    recipe_manager = RecipeManager()  # Конкретно-прикладной менеджер

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('RecipeHub:recipe_detail', args=[self.name])


# 2. Модель - модель отзывов (модель для отзывов)
class Reviews(models.Model):
    tuple_of_ratings = (
        ('1 звезда', '1☆'),
        ('2 звезды', '2☆'),
        ('3 звезды', '3☆'),
        ('4 звезды', '4☆'),
        ('5 звезд', '5☆'),
    )

    recipe = models.ForeignKey(
        Post_recipe,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    grade = models.CharField(
        max_length=50,
        choices=tuple_of_ratings,
        verbose_name="Оценка пользователя",
        help_text="Оцените данный рецепт"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    comments = models.TextField(
        verbose_name="Комментарии",
        help_text="Оставьте ваши комментарии"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.grade} - {str(self.comments)[:20]}..."

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

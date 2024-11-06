from django.db import models
from datetime import timedelta
from django.urls import reverse
# Менеджер для рецептов 
class RecipeManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_vegetarian=True)\
        .filter(is_fast_food=True)\
        .filter(is_dessert=True)
    
# Менеджер для отзывов
class ReviewManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(grade__in=['5 звезд', '4 звезды'])

# TODO: Добавить если рецептов 10+ перемещать их на новую созданную страницу, также с отзывами, лучшими рецептами
# TODO: поле кбжу ккал
# TODO: горячее или холодное блюдо
# TODO: гарнир
# TODO: возможно напитки 
# TODO: ОСТАВИТЬ КОММЕНТАРИИ НА ОТЗЫВ
# TODO: разделять побуквенно на рецепты , то есть юзер по букве может найти блюдо
# 1. Модель - основная модель данных моих рецептов
class Post_recipe(models.Model):
    #TODO: в бд
    DISH_LVL = (
        ('Очень просто', 'Очень просто'),
        ('Просто', 'Просто'),
        ('Средней сложности', 'Средней сложности'),
        ('Сложно', 'Сложно'),
        ('Очень сложно', 'Очень сложно'),
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
        default=False,
        help_text="Проставьте галочку если это относится к этой категории"
    )

    is_fast_food = models.BooleanField(
        verbose_name="Еда быстрого приготовления?",
        default=False,
        help_text="Проставьте галочку если это относится к этой категории"
    )

    is_dessert = models.BooleanField(
        verbose_name="Данная еда являетя десертом?",
        default=False,
        help_text="Проставьте галочку если это относится к этой категории"
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
    )

    steps = models.TextField(
        verbose_name='Шаги приготовления',
        blank=False,
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
        help_text='Загрузите фото данного блюда.'  #TODO: Нужно добавить валидаторы для конвертации картинки.
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

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


# 2. Модель - модель моих отзывов
class Reviews(models.Model):
    # TODO: в бд
    tuple_of_ratings = (
        ('1 звезда', '1☆'),
        ('2 звезды', '2☆'),
        ('3 звезды', '3☆'),
        ('4 звезды', '4☆'),
        ('5 звезд', '5☆'),
    )
     
    author = models.CharField(
        verbose_name='Автор',
        max_length=30,
        unique=True,
        blank=True,
        help_text="По вашему желанию можете указать автора данного рецепта"
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
    
    objects = models.Manager() #  # Менеджер, применяемый по умолчанию
    review_manager = ReviewManager()  # Конкретно-прикладной менеджер для моих отзыв

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.grade} - {str(self.comments)[:20]}..."

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

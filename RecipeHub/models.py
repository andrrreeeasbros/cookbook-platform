from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from PIL import Image, ImageEnhance, ImageFilter
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from django.contrib.auth.models import User


class RecipeManager(models.Manager):
    def filter_by_category(self, category_name):
        return self.get_queryset().filter(categories__name=category_name)

    def filter_by_cuisine(self, cuisine_name):
        return self.get_queryset().filter(cuisines__name=cuisine_name)

    def filter_by_category_and_cuisine(self, category_name, cuisine_name):
        return self.get_queryset().filter(categories__name=category_name, cuisines__name=cuisine_name)

class UserProfileManager(models.Manager):
    def all_profiles(self):
        return self.all()


class ReviewManager(models.Manager):
    def get_average_rating(self, recipe):
        reviews = self.filter(recipe=recipe)
        if reviews.exists():
            total_grade = sum([review.grade.value for review in reviews])
            average_rating = total_grade / reviews.count()
            if average_rating > 4:
                return average_rating
        return 0
    


class Category(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name}"


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Cuisine(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Кухня мира"
        verbose_name_plural = "Кухни мира"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название ингредиента')

    def __str__(self):
        return f"{self.name}"


class Likes_recipes(models.Model):
    pass


class Post_recipe(models.Model):
    name = models.CharField(
        verbose_name='Название блюда',
        primary_key=True,
        max_length=30,
    )

    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории блюда',
        related_name='recipes',
        blank=True,
        help_text="Выберите категории, которые подходят для этого рецепта"
    )

    cuisines = models.ManyToManyField(
        Cuisine,
        verbose_name="Кухни мира",
        related_name="recipes",
        blank=True,
        help_text="Выберите кухни мира для этого рецепта"
    )

    level = models.ForeignKey(
        DifficultyLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Уровень сложности',
    )

    ingredients_list = models.TextField(
        max_length=1500,
        verbose_name='Ингредиенты',
        blank=True,
        null=True
    )

    steps = models.TextField(
        verbose_name='Шаги приготовления',
        blank=False,
    )

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления блюда',
        default=timedelta(minutes=30),
        help_text='Напишите примерное время приготовления данного блюда(в минутах)',
        validators=[MinValueValidator(0)]
    )

    dish_photo = models.ImageField(
        unique=True,
        verbose_name='Фото блюда',
        upload_to='dish_photos/',
        height_field=None,
        width_field=None,
        help_text='Загрузите фото данного блюда.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def change_register(self):
        return f"{self.name.capitalize()}"

    def minutes_to_hours_to_days(self):
        if isinstance(self.cooking_time, int):
            if self.cooking_time >= 1440:
                days = self.cooking_time // 1440
                remaining_minutes = self.cooking_time % 1440
                hours = remaining_minutes // 60
                minutes = remaining_minutes % 60
                return f'{days} дн. {hours} ч. {minutes} мин.'
            elif self.cooking_time >= 60:
                hours = self.cooking_time // 60
                minutes = self.cooking_time % 60
                return f"{hours} ч. {minutes} мин."
            else:
                return f"{self.cooking_time} мин."
        else:
            return "Некорректное время"

    def save(self, *args, **kwargs):
        self.name = self.change_register()

        super().save(*args, **kwargs)

        if self.dish_photo:
            self.resize_image()

    def resize_image(self):

        image_path = self.dish_photo.path
        img = Image.open(image_path)

        img = img.resize((674, 446), Image.Resampling.LANCZOS)

        img.save(image_path)
    
    def enhance_image_quality(self):
        image_path = self.dish_photo.path
        img = Image.open(image_path)
        
        enhancer_sharp = ImageEnhance.Sharpness(img)
        img = enhancer_sharp.enhance(2.0)  # Увеличиваем резкость в 2 раза
        
        enhancer_contrast = ImageEnhance.Contrast(img)
        img = enhancer_contrast.enhance(1.5)  # Увеличение контраста
        
        img = img.filter(ImageFilter.MedianFilter(3))  # Применяем медианный фильтр для уменьшения шума

        img.save(image_path)

    objects = RecipeManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('RecipeHub:recipe_detail', args=[self.name])


class Grade(models.Model):
    value = models.IntegerField()
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.display_name}"


class Comments(models.Model):
    pass 

class Likes_reviews(models.Model):
    pass

class Reviews(models.Model):
    author = models.CharField(
        verbose_name='Автор',
        max_length=30,
    )

    recipe = models.ForeignKey(
        Post_recipe,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
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

    objects = models.Manager()  # Менеджер, применяемый по умолчанию
    review_manager = ReviewManager()  # Конкретно-прикладной менеджер для моих отзыв

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.grade} - {str(self.comments)[:20]}..."

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Timezone(models.Model):
    country = models.CharField(max_length=100, unique=True)
    timezone = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.country} - {self.timezone}'

    class Meta:
        verbose_name = "Timezone"
        verbose_name_plural = "Timezones"


class Age(models.Model):
    years = models.IntegerField(
        verbose_name="Возраст",
        help_text="Введите возраст",
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )

    def __str__(self):
        return f'{self.years}'

    class Meta:
        verbose_name = 'Age'
        verbose_name_plural = 'Ages'


class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        related_name="profile",
        verbose_name="Пользователь"
    )

    name = models.CharField(
        verbose_name="Имя автора профиля",
        unique=True,
        max_length=20,
        help_text='Введите ваше имя'
    )

    country = models.ForeignKey(
        Timezone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна",
        help_text="Введите вашу страну"
    )

    age = models.ForeignKey(
        Age,
        verbose_name="Возраст",
        help_text="Ваш возраст",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name="Описание",
        max_length=500,
        help_text="Описание пользователя"
    )

    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )

    profile_photo = models.ImageField(
        verbose_name="Фото профиля",
        upload_to="media/profile_photo",
        default='static/css/img/profile.png',
        help_text="Загрузите ваше фото"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    profiles = UserProfileManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.name if len(self.name) <= 10 else f"{self.name[:10]}..."


class TeamConnection(models.Model):
    pass


# TODO: Заполнить forms.py и сделать кнопки рабочими
# TODO: Сделать расположение по алфовитному порядку в "Все рецепты"
# TODO: вместо def НА КЛАССЫ В ВЬЮШКАХ
# TODO: Проработать библиотку с избежанием мат слов
# TODO: Класс своего аккаунта(Добавить папку избранное в профиле + Добавить возможность пользователям ставить друг другу "лайки" на рецепты или на отзывы)
# TODO: ОСТАВИТЬ КОММЕНТАРИИ НА ОТЗЫВ
# TODO: разделять побуквенно на рецепты , то есть юзер по букве может найти блюдо
# TODO: Модель связи с админами в contacts.html
# TODO: Настроить админ панель
# TODO: Добавить рандомный рецепт + поиск рецептов

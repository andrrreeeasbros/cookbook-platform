from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
import re
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from PIL import Image
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class RecipeManager(models.Manager):
    pass


class VegetarianRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Вегетарианское блюдо")


class QuickRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Еда быстрого приготовления")


class DessertRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Десерт")


class VeganRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Веганское")


class DrinkRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Напитки")


class SnackRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Закуски")


class SideDishRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Гарниры")


class BakingRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__name="Печенье и выпечка")


class ItalianRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Итальянская")


class FrenchRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Французская")


class JapaneseRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Японская")


class ChineseRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Китайская")


class MexicanRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Мексиканская")


class ThaiRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Тайская")


class IndianRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Индийская")


class GreekRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Греческая")


class SpanishRecipeManager(RecipeManager):
    def get_queryset(self):
        return super().get_queryset().filter(cuisines__name="Испанская")

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
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class DifficultyLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кухня мира"
        verbose_name_plural = "Кухни мира"


# class Likes(models.Model):
#     pass


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
        verbose_name='Ингредиенты данного рецепта',
        max_length=2000,
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
        return self.name.capitalize()

    def split_text(self):
        patterns = [
            "Подготовка моллюсков", "Приготовление пасты", "Готовим соус",
            "Добавление моллюсков и вина", "Смешивание пасты с соусом", "Подача",
            "Промывание моллюсков", "Проверка моллюсков на живость", "Вскипятить воду",
            "Отварить пасту", "Разогреть оливковое масло", "Обжарить чеснок", "Добавить чили",
            "Накрыть крышкой", "Готовить на среднем огне", "Добавить готовую пасту",
            "Перемешать пасту с соусом", "Посыпать петрушкой", "Приправить солью и перцем",
            "Подавать с лимоном", "Нарезать чеснок", "Обжаривать до золотистого цвета",
            "Не пережаривать чеснок", "Использовать белое вино", "Готовить 5-7 минут",
            "Проверить моллюсков", "Закрыть крышкой", "Дать настояться", "Подавать немедленно",
            "Очищение овощей", "Нарезка кубиками", "Жарить на сильном огне", "Кипятить бульон",
            "Добавить специи", "Тушить", "Замариновать мясо", "Выложить на тарелку",
            "Сервировать", "Режем кольцами", "Варить на пару", "Готовить в духовке",
            "Мелко нарезать", "Резать ломтями", "Измельчить зелень", "Фаршировать",
            "Пожарить до хрустящей корочки", "Подогреть", "Слегка подрумянить", "Добавить в воду",
            "Завернуть в фольгу", "Крошить сыр", "Приготовить к жарке", "Печь в духовке",
            "Протереть через сито", "Взбить до пены", "Готовить на гриле", "Обработать блендером",
            "Легко обжарить", "Налить в форму", "Пропарить", "Растирать в ступке", "Приготовить соус на основе бульона",
            "Использовать чесночный порошок", "Разделить на порции", "Обжаривать на масле", "Украсить зеленью",
            "Подсушить хлеб", "Разогреть сковороду", "Добавить масло", "Приготовить в аэрогриле",
            "Подготовить специи", "Включить таймер", "Режем соломкой", "Отварить яйца", "Использовать остроту чили",
            "Тушить на медленном огне", "Сделать крем", "Разделить на части", "Размять пюре", "Вымешать тесто",
            "Выпекать до готовности", "Карамелизовать", "Полить медом", "Приготовить шницель", "Устроить дегустацию",
            "Замораживать ингредиенты", "Протереть на терке", "Использовать свежие травы", "Нарезать пластинами",
            "Поджарить бекон", "Вскипятить молоко", "Убрать из кастрюли", "Готовить в пароварке", "Прокипятить вино",
            "Охладить перед подачей", "Притушить до мягкости", "Готовить на огне", "Завернуть в тесто", "Взбить яйца с сахаром",
            "Добавить свежие овощи", "Подготовить ингредиенты", "Заварить чай", "Очистить рыбу", "Порезать ломтями",
            "Измельчить орехи", "Разогреть жаровню", "Приготовить пудинг", "Подогреть суп", "Подсушить орехи",
            "Смешать все компоненты", "Готовить на сковороде", "Готовить на медленном огне", "Использовать специи по вкусу",
            "Нарезать мелко", "Печь в печи", "Выложить на противень", "Вылить в кастрюлю", "Готовить с добавлением меда",
            "Высыпать муку в миску", "Приготовить мясо на гриле", "Покрошить в салат", "Приправить зеленью", "Налить соус",
            "Тонко нарезать", "Взбить венчиком", "Замесить тесто", "Отправить в морозильник", "Выложить на тарелку с соусом",
            "Разогревать кастрюлю", "Налить в чашку", "Обжарить на сковороде с маслом", "Сформировать котлеты", "Нарезать полосками",
            "Запечь до золотистой корочки", "Готовить в мультиварке", "Смешать с мукой", "Добавить мед или сахар",
            "Подготовить противень", "Обернуть в пленку", "Порезать кольцами", "Кипятить воду с солью", "Тонко нарезать овощи",
            "Положить в кастрюлю", "Готовить до мягкости", "Залить соусом", "Прокипятить на медленном огне", "Обработать овощи",
            "Готовить на пару до готовности", "Нарезать мясо ломтями", "Приготовить десерт", "Запечь в фольге", "Использовать приправы",
            "Сделать подливку", "Обжаривать до хрустящей корочки", "Положить в духовку", "Готовить в сковороде на оливковом масле",
            "Нарезать зелень", "Подавать с соусом", "Залить горячим бульоном", "Сформировать форму для запеканки", "Обработать мясо специями",
            "Варить до готовности", "Разогреть духовку до 180 градусов", "Использовать лимонный сок", "Готовить на большой температуре",
            "Нарезать поперек", "Перемешать все ингредиенты", "Сделать пасту", "Завернуть в пергамент", "Приготовить по рецепту",
            "Порезать на кусочки", "Разогреть масло", "Смешать с уксусом", "Подавать горячим", "Сделать карри", "Положить в кастрюлю",
            "Порезать хлеб", "Разложить по тарелкам", "Отправить в холодильник", "Измельчить на блендере", "Приготовить соус для пасты",
            "Украсить соусом", "Готовить с оливковым маслом", "Пропустить через мясорубку", "Обжарить до румяной корочки", "Сервировать на столе",
            "Печь в микроволновке", "Приготовить картофельное пюре", "Готовить в кастрюле", "Разогреть масло в кастрюле", "Залить водой",
            "Провести дегустацию", "Приготовить картофельное пюре", "Протереть овощи", "Печь до готовности", "Порезать на небольшие кусочки",
            "Готовить с помидорами", "Растерзать мясо", "Очищать овощи", "Приготовить бульон"
        ]

        s = self.steps
        if isinstance(self.steps, str):
            s = re.sub(r'\s+', ' ', self.steps.strip())
            s = re.sub(r'\.(?=\s|$)', '.\n', s)

        split_steps = s.split('\n')

        result = []
        for line in split_steps:
            if any(pattern in line for pattern in patterns):
                result.append(line.strip())
            else:
                result.append(line.strip())

        return "\n".join(result)

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
        self.steps = self.split_text()

        super().save(*args, **kwargs)

        if self.dish_photo:
            self.resize_image()

    def resize_image(self):

        image_path = self.dish_photo.path
        img = Image.open(image_path)

        img = img.resize((674, 446), Image.Resampling.LANCZOS)

        # Сохраняем измененное изображение
        img.save(image_path)

    recipe_manager = RecipeManager()
    objects = models.Manager()

    italian_manager = ItalianRecipeManager()
    french_manager = FrenchRecipeManager()
    japanese_manager = JapaneseRecipeManager()
    chinese_manager = ChineseRecipeManager()
    mexican_manager = MexicanRecipeManager()
    thai_manager = ThaiRecipeManager()
    indian_manager = IndianRecipeManager()
    greek_manager = GreekRecipeManager()
    spanish_manager = SpanishRecipeManager()

    vegetarian_manager = VegetarianRecipeManager()
    quick_manager = QuickRecipeManager()
    dessert_manager = DessertRecipeManager()  # Менеджер для десертов
    vegan_manager = VeganRecipeManager()  # Менеджер для веганских рецептов
    drink_manager = DrinkRecipeManager()  # Менеджер для напитков
    snack_manager = SnackRecipeManager()  # Менеджер для закусок
    side_dish_manager = SideDishRecipeManager()  # Менеджер для гарниров
    baking_manager = BakingRecipeManager()  # Менеджер для печенья и выпечки

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
        return self.display_name

# class Likes(models.Model):
#     pass


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
        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)
        
    profiles = UserProfileManager()    
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        # Возвращаем имя, если оно длиннее 10 символов, добавляем многоточие
        return self.name if len(self.name) <= 10 else f"{self.name[:10]}..."
    

class TeamConnection(models.Model):
    pass

# TODO: Заполнить категории всеми рецептами кухонь +15 + добавить "поиск кухни" поле
# TODO: Сделать расположение по алфовитному порядку в "Все рецепты"
# TODO: Сделать поле для время перекуса
# TODO: изменить поле время готовки чтоб не было отрицательным
# TODO: вместо def НА КЛАССЫ В ВЬЮШКАХ
# TODO: Исправить лого в мой профиль
# TODO: Проработать библиотку с избежанием мат слов
# TODO: Нужно добавить валидаторы для конвертации картинки.
# TODO: Класс своего аккаунта(Добавить папку избранное в профиле + Добавить возможность пользователям ставить друг другу "лайки" на рецепты или на отзывы)
# TODO: Заполнить кнопку посмотреть отзывы
# TODO: Добавить пагинацию если 2+ лучших рецептов
# TODO: поле кбжу ккал
# TODO: ОСТАВИТЬ КОММЕНТАРИИ НА ОТЗЫВ
# TODO: разделять побуквенно на рецепты , то есть юзер по букве может найти блюдо
# TODO: Заполнить forms.py и сделать кнопки рабочими
# TODO: Модель связи с админами в contacts.html
# TODO: Настроить админ панель
# TODO: Заполнить categories_list
# TODO: Заполнить tests.py
# TODO: Пагинация: Разделить рецепты на страницы для ускорения загрузки.

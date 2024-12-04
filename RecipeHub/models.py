from django.db import models
from django.utils import timezone
from datetime import timedelta
from zoneinfo import ZoneInfo
from django.urls import reverse
import logging
from multiselectfield import MultiSelectField
import re


class RecipeManager(models.Manager):  # Менеджер для рецептов
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_vegetarian=True)\
            .filter(is_fast_food=True)\
            .filter(is_dessert=True)


class ReviewManager(models.Manager):  # Менеджер для отзывов
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(grade__in=['5★', '4★']).distinct()


class Post_recipe(models.Model):  # 1. Модель - основная модель данных моих рецептов
    DISH_LVL = (
        ('Очень просто', 'Очень просто'),
        ('Просто', 'Просто'),
        ('Средней сложности', 'Средней сложности'),
        ('Сложно', 'Сложно'),
        ('Очень сложно', 'Очень сложно'),
    )

    DISH_CATEGORIES = (
        ('vegetarian', 'Вегетарианское блюдо'),
        ('fast_food', 'Еда быстрого приготовления'),
        ('dessert', 'Десерт'),
        ('vegan', 'Веганское'),
        ('drinks', 'Напитки'),
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
    )

    WORLD_CUISINE_CATEGORIES = (
        ('italian', 'Итальянская кухня'),
        ('japanese', 'Японская кухня'),
        ('mexican', 'Мексиканская кухня'),
        ('chinese', 'Китайская кухня'),
        ('indian', 'Индийская кухня'),
        ('french', 'Французская кухня'),
        ('greek', 'Греческая кухня'),
        ('arabic', 'Арабская кухня'),
        ('american', 'Американская кухня'),
    )

    name = models.CharField(
        verbose_name='Название блюда',
        primary_key=True,
        max_length=30,
    )

    categories = MultiSelectField(
        verbose_name='Категории блюда',
        choices=DISH_CATEGORIES,
        max_length=100,
        help_text="Выберите категории, которые подходят для этого рецепта",
        default=[],
    )

    world_cuisine_categories = MultiSelectField(
        verbose_name='Кухни мира',
        choices=WORLD_CUISINE_CATEGORIES,
        max_length=100,
        help_text="Выберите кухни мира, если выбрана категория 'По кухне мира'",
        default=[],
        blank=True,
    )

    meal_time = models.CharField(
        verbose_name='Время приёма пищи',
        choices=[('breakfast', 'Завтрак'),
                 ('lunch', 'Обед'), ('dinner', 'Ужин')],
        max_length=10,
        blank=True,  # Поле может быть пустым
        help_text="Выберите только одно время приёма пищи (завтрак, обед или ужин).",
    )

    level = models.CharField(
        verbose_name='Уровень сложности',
        choices=DISH_LVL,
        max_length=20
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

    objects = models.Manager()  # Менеджер, применяемый по умолчанию
    recipe_manager = RecipeManager()  # Конкретно-прикладной менеджер

    def change_register(self):
        s = self.name
        logging.debug(f"Original name: {s}")  # Логирование исходного значения
        if s and s[0].islower():  # Проверка на непустоту и на то, что первая буква строчная
            # Заглавная первая буква, остальные без изменений
            s = s[0].upper() + s[1:]
            # Логирование изменённого значения
            logging.debug(f"Changed name: {s}")
        return s

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
            "Проверить моллюсков", "Закрыть крышкой", "Дать настояться", "Подавать немедленно"
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

    def save(self, *args, **kwargs):
        if 'world_cuisine' in self.categories and not self.world_cuisine_categories:
            raise ValueError("Пожалуйста, выберите хотя бы одну кухню мира.")
        self.name = self.change_register()

        self.steps = self.split_text()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('RecipeHub:recipe_detail', args=[self.name])


class Reviews(models.Model):  # 2. Модель - модель моих отзывов
    tuple_of_ratings = (
        ('1★', '1★'),
        ('2★', '2★'),
        ('3★', '3★'),
        ('4★', '4★'),
        ('5★', '5★'),
    )

    author = models.CharField(
        verbose_name='Автор',
        max_length=30,
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


class UserProfile(models.Model):
    name = models.CharField(
        verbose_name="Имя автора профиля",
        unique=True,
        max_length=20,
        help_text='Введите ваше имя'
    )
    TIMEZONE_MAP = {
        'Армения': 'Asia/Yerevan',  # Армения
        'Азербайджан': 'Asia/Baku',  # Азербайджан
        'Беларусь': 'Europe/Minsk',  # Беларусь
        'Казахстан': 'Asia/Almaty',  # Казахстан
        'Кыргызстан': 'Asia/Bishkek',  # Кыргызстан
        'Молдова': 'Europe/Chisinau',  # Молдова
        'Россия': 'Russia',  # Россия
        'Таджикистан': 'Asia/Dushanbe',  # Таджикистан
        'Туркменистан': 'Asia/Ashgabat',  # Туркменистан
        'Украина': 'Europe/Kiev',  # Украина
        'Узбекистан': 'Asia/Tashkent',  # Узбекистан
    }

    TIMEZONE_MAP2 = {
        'Russia (Moscow)': 'Europe/Moscow',
        'Russia (Saint Petersburg)': 'Europe/Moscow',
        'Russia (Far East)': 'Asia/Vladivostok',
        'Russia (Siberia)': 'Asia/Irkutsk',
        'Russia (Ural)': 'Asia/Yekaterinburg',
        'Russia (Krasnoyarsk)': 'Asia/Krasnoyarsk',
    }

    country = models.CharField(
        verbose_name="Страна",
        max_length=50,
        choices=TIMEZONE_MAP.items(),  # Это будет кортеж пар (ключ, значение)
        help_text="Введите вашу страну"
    )

    age_choices = [(i, str(i)) for i in range(1, 101)]

    age = models.IntegerField(
        verbose_name="Возраст",
        choices=age_choices,
        help_text="Ваш возраст"
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

    def change_zone(self):
        country = self.country
        if country in self.TIMEZONE_MAP:
            if country == 'Russia':
                zone_info = ZoneInfo(self.TIMEZONE_MAP2.get(
                    f"Russia ({country})", "UTC"))
            else:
                zone_info = ZoneInfo(self.TIMEZONE_MAP[country])
        else:
            zone_info = ZoneInfo("UTC")

        self.created_at = timezone.localtime(self.created_at, zone_info)

    def save(self, *args, **kwargs):
        """
        Переопределённый метод save для корректной обработки временной зоны.
        """
        if not self.created_at:
            self.created_at = timezone.now()

        # Применяем временную зону, если она не была задана
        self.change_zone()  # Меняем временную зону в зависимости от страны
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.name[:10]


# class TeamConnection(models.Model):
#     pass


# class Likes(models.Model):
#     pass


# TODO: УБРАТЬ ЧТОБ НЕ БЫЛО ЛИШНИХ ПРОБЕЛОВ В РЕЦЕПТАХ И ЛУЧШИХ РЕЦЕПТАХ
# TODO: ДОДЕЛАТЬ ВЕРТСКУ + поправить полоску лого в categories.css + исправить reviews.css
# TODO: js эффекты для файлов
# TODO: Нужно добавить валидаторы для конвертации картинки.
# TODO: Класс своего аккаунта(Добавить папку избранное в профиле + Добавить возможность пользователям ставить друг другу "лайки" на рецепты или на отзывы)
# TODO: Класс для общего рейтенга лучшего рецепта если общее число рейтенга <4
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

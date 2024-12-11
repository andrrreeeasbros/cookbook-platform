from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
import re
from django.core.validators import MinValueValidator, MaxValueValidator


<<<<<<< HEAD
class RecipeManager(models.Manager):  
    pass

=======
class RecipeManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_vegetarian=True)\
            .filter(is_fast_food=True)\
            .filter(is_dessert=True)
<<<<<<< HEAD
>>>>>>> dadb929109da20cc0ca311ef890b7babe11c4f19
class ReviewManager(models.Manager):  
=======


class ReviewManager(models.Manager):
>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(grade__in=[4, 5]).distinct()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_default_categories(cls):
        categories = [
            'Вегетарианское блюдо',
            'Еда быстрого приготовления',
            'Десерт',
            'Веганское',
            'Напитки',
            'Завтрак',
            'Обед',
            'Ужин',
        ]
        for category_name in categories:
            cls.objects.get_or_create(name=category_name)
        
class DifficultyLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

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
<<<<<<< HEAD
        related_name='recipes',
=======
        choices=(
            ('vegetarian', 'Вегетарианское блюдо'),
            ('fast_food', 'Еда быстрого приготовления'),
            ('dessert', 'Десерт'),
            ('vegan', 'Веганское'),
            ('drinks', 'Напитки'),
            ('breakfast', 'Завтрак'),
            ('lunch', 'Обед'),
            ('dinner', 'Ужин'),
        ),
        max_length=100,
        help_text="Выберите категории, которые подходят для этого рецепта",
        default=[],
    )

    world_cuisine_categories = MultiSelectField(
        verbose_name='Кухни мира',
        choices=(
            ('italian', 'Итальянская кухня'),
            ('japanese', 'Японская кухня'),
            ('mexican', 'Мексиканская кухня'),
            ('chinese', 'Китайская кухня'),
            ('indian', 'Индийская кухня'),
            ('french', 'Французская кухня'),
            ('greek', 'Греческая кухня'),
            ('arabic', 'Арабская кухня'),
            ('american', 'Американская кухня'),
        ),
        max_length=100,
        help_text="Выберите кухни мира, если выбрана категория 'По кухне мира'",
        default=[],
>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
        blank=True,
        help_text="Выберите категории, которые подходят для этого рецепта"
    )

<<<<<<< HEAD
    level = models.ForeignKey(
        DifficultyLevel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
        )
    
=======
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
        choices=(
            ('Очень просто', 'Очень просто'),
            ('Просто', 'Просто'),
            ('Средней сложности', 'Средней сложности'),
            ('Сложно', 'Сложно'),
            ('Очень сложно', 'Очень сложно'),
        ),
        max_length=20
    )

>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
    ingredients_list = models.TextField(
        verbose_name='Ингредиенты данного рецепта',
        max_length=2000,
    )

    steps = models.TextField(
        verbose_name='Шаги приготовления',
        blank=False,
    )

<<<<<<< HEAD
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления блюда',
        default=timedelta(minutes=30),
        help_text='Напишите примерное время приготовления данного блюда(в минутах)',
        validators=[MinValueValidator(0)]
    )

=======
>>>>>>> dadb929109da20cc0ca311ef890b7babe11c4f19
    dish_photo = models.ImageField(
        unique=True,
        verbose_name='Фото блюда',
        upload_to='dish_photos/',
        height_field=None,
        width_field=None,
        help_text='Загрузите фото данного блюда.'
    )
    
    cooking_time = models.DurationField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    objects = models.Manager()  
    recipe_manager = RecipeManager()  

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
<<<<<<< HEAD
    
    def minutes_to_hours_to_days(self):
        if self.cooking_time >= 1440:
            days = self.cooking_time // 1440
            remaining_minutes = self.cooking_time % 1440
            hours = remaining_minutes // 60
            minutes = remaining_minutes % 60
            return f'{days} дней {hours} часов {minutes} минут'
        elif self.cooking_time >= 60:
            hours = self.cooking_time // 60
            minutes = self.cooking_time % 60
            return f"{hours} часов {minutes} минут"
        else:
            return f"{self.cooking_time} минут"

 
    def save(self, *args, **kwargs):
<<<<<<< HEAD
=======
        
=======

    def clean_bad_words(self):
        text_fields = [self.name, self.ingredients_list, self.steps]

        bad_list = ["Урод", "Тупой", "Придурок", "Чмо"]

        cleaned_fields = []

        for field in text_fields:
            cleaned_field = ' '.join(
                [len(word) * "*" if word.lower() in [bad_word.lower()
                                                     for bad_word in bad_list] else word for word in field.split()]
            )
            cleaned_fields.append(cleaned_field)

        return cleaned_fields

    def save(self, *args, **kwargs):
        if 'world_cuisine' in self.categories and not self.world_cuisine_categories:
            raise ValueError("Пожалуйста, выберите хотя бы одну кухню мира.")

        cleaned_fields = self.clean_bad_words()

        clean_text = " ".join([str(field).strip() for field in cleaned_fields])

        if profanity.contains_profanity(clean_text):
            raise ValidationError('Матерные слова не допустимы')

>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
>>>>>>> dadb929109da20cc0ca311ef890b7babe11c4f19
        self.name = self.change_register()
        self.steps = self.split_text()

        super().save(*args, **kwargs)

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

<<<<<<< HEAD
    def __str__(self):
        return self.display_name   

# class Likes(models.Model):
#     pass

class Reviews(models.Model):  
=======
class Reviews(models.Model):
>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
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

<<<<<<< HEAD
    grade = models.ForeignKey(
        Grade,  
        on_delete=models.CASCADE,  
=======
    grade = models.CharField(
        max_length=50,
        choices=(
            ('★', '1★'),
            ('★★', '2★'),
            ('★★★', '3★'),
            ('★★★★', '4★'),
            ('★★★★★', '5★'),
        ),
>>>>>>> 10af2ddf79176b7368e15ae5346368dc6a9230af
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
    name = models.CharField(
        verbose_name="Имя автора профиля",
        unique=True,
        max_length=20,
        help_text='Введите ваше имя'
    )
   
    country = models.ForeignKey(
        Timezone,  # Связь с моделью Timezone
        on_delete=models.SET_NULL,  # Если Timezone удален, не удалять UserProfile
        null=True,  # Разрешаем пустое значение
        blank=True,  # Разрешаем пустое значение
        verbose_name="Страна",
        help_text="Введите вашу страну"
    )

    age = models.ForeignKey(
        Age,
        verbose_name="Возраст",
        help_text="Ваш возраст",
        on_delete=models.SET_NULL,  # Если объект Age будет удален, оставляем UserProfile
        null=True,  # Разрешаем пустое значение
        blank=True  # Разрешаем пустое значение
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

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.name[:10]


# class TeamConnection(models.Model):
#     pass

# TODO: Использовать block для logo html
# TODO: Придумать как распределять рецепты по критериям
# TODO: изменить поле время готовки чтоб не было отрицательным 
# TODO: Убрать все choice и переписать под фикстуры 
# TODO: вместо def НА КЛАССЫ В ВЬЮШКАХ 
# TODO: Класс для общего рейтенга лучшего рецепта если общее число рейтенга <4
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

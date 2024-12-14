from django.apps import AppConfig

class RecipehubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'RecipeHub'

    def ready(self):
        """
        Этот метод вызывается, когда приложение готово к работе.
        Здесь можно выполнять задачи по настройке, например, подключать сигналы.
        """
        # Пример: Подключение сигналов, если они есть
        # from . import signals
        pass

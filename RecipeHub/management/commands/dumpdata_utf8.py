import json
from django.core.management.base import BaseCommand
from django.core.management.commands.dumpdata import Command as DumpDataCommand

class Command(BaseCommand):
    help = 'Export data in UTF-8 encoded JSON'

    def handle(self, *args, **options):
        # Создаем объект команды dumpdata
        command = DumpDataCommand()

        # Вытягиваем вывод данных, использовав стандартную логику команды dumpdata
        output = command.get_data(*args, **options)

        # Открываем файл и записываем данные с ensure_ascii=False
        with open('RecipeHub/fixtures/RecipeHub/data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS('Data exported successfully in UTF-8!'))

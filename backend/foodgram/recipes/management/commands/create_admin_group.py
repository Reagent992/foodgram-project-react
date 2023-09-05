from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Устанавливает права для групп пользователей Администратор"

    def handle(self, *args, **options):
        try:
            models = ('user', 'recipe', 'ingredients', 'tag',)
            admin, created = Group.objects.get_or_create(name='admin')
            if created:
                permissions = list()
                for model in models:
                    permissions.extend(Permission.objects.filter(
                        content_type__model=model))

                admin.permissions.set(permissions)
            self.stdout.write(
                self.style.SUCCESS('Группа создана.')
            )

        except CommandError as error:
            self.stdout.write(
                self.style.ERROR(f'Ошибка установки прав: {error}'))

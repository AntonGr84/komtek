from django.contrib.auth import models
from django.core.management import base


class Command(base.BaseCommand):
    """Пользовательская команда для инициплизации суперпользователя
    """
    def handle(self, *args, **options):
        if models.User.objects.count() == 0:
            username: str = 'admin'
            email = 'admin@example.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin: models.User = models.User.objects.create_superuser(
                username, email=email, password=password
            )
            admin.save()
        else:
            print(
                'Admin accounts can only be initialized if no Accounts exist'
            )

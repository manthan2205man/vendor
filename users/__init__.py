default_app_config = 'users.apps.UsersConfig'

from django.apps import apps

def ready():
    from users import signals  # Import signals here
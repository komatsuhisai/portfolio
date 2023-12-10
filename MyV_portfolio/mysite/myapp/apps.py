from django.apps import AppConfig


class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import signals  # これによりsignals.pyがインポートされます


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

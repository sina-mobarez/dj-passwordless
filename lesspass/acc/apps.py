from django.apps import AppConfig


class AccConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acc'

    def ready(self):
        # Importing signals to ensure they are connected
        import acc.signals

        # Importing tasks to ensure they are registered with the task queue
        import acc.tasks

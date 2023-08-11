from django.apps import AppConfig



class JudgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'judge'

    def ready(self):
        import judge.signals  # Import signals module #saving a model instance of userfrofile

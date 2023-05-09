from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'orders'


    """
    we would normally wire the container here, but we are doing it from the main project file, after all apps have
    been loaded; 
    this is because of a bug in the dependency injector when the dependency contains models from other apps
    and additionally we do not want to create a dependency to the main project file, keeping the app loosely coupled 
    """
    # def ready(self):
    #    from swd_django_demo import container  # <-- import the container here so further imports inside container.py like models can succeed
    #    container.wire(modules=[".views"])

from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "properties"

    def ready(self):
        """
        This method is called when the application is ready.
        It can be used to perform application initialization tasks.
        """
        # Import signals to ensure they are registered
        import properties.signals  # Ensure signals are imported to register them
        print("Properties app is ready and signals are imported.")    

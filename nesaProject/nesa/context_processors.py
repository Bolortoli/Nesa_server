from .models import Settings

def global_settings(request):
    return {
        'global_settings': Settings.objects.all()[0]
    }
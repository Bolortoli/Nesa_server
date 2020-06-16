from django.contrib import admin
from .models import ContactUs, ActiveServers, Reward, Settings

# Register your models here.
admin.site.register(ContactUs)
admin.site.register(ActiveServers)
admin.site.register(Reward)
admin.site.register(Settings)
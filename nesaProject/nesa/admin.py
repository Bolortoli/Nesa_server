from django.contrib import admin
from .models import ContactUs, ActiveServers, Reward, Settings, ServerCategory
from django.db import models
from django.forms import Textarea, TextInput

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'email', 'phone', 'text'] 
    list_display_links = None
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ServerCategory)

class ActiveServersAdmin(admin.ModelAdmin):
    list_display = ['name', 'pic', 'category', 'server_type']
    list_editable = ['server_type']

admin.site.register(ActiveServers, ActiveServersAdmin)

class RewardsAdmin(admin.ModelAdmin):
    list_display = ['title', 'serName', 'year', 'month', 'slug'] 
    # list_display_links = None

admin.site.register(Reward, RewardsAdmin)

class SettingsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Settings._meta.get_fields()]
    list_editable = [f.name for f in Settings._meta.get_fields() if f.name != "id" and f.name != "title"]
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Settings, SettingsAdmin)


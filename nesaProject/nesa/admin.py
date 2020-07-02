from django.contrib import admin
from .models import ContactUs, ActiveServers, Reward, Settings


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'email', 'phone', 'text'] 
    list_display_links = None
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ContactUs, ContactUsAdmin)

# class ActiveServersAdmin(admin.ModelAdmin):
#     list_display = ['name','address']
#     list_editable = ['address','city','state']
admin.site.register(ActiveServers)
admin.site.register(Reward)
admin.site.register(Settings)

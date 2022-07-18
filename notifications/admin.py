from django.contrib import admin

# Register your models here.

from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    fields = ['receiver', 'subject', 'text']
    list_display = ('receiver', 'subject')

admin.site.register(Notification, NotificationAdmin)
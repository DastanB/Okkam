from django.contrib import admin

from .models import WebPage

# Register your models here.
@admin.register(WebPage)
class WebPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'ip_address', 'http_code', 'timeout','created_at', 'updated_at')
    search_fields = ('url', 'ip_address', 'http_code')
    list_filter = ('http_code',)
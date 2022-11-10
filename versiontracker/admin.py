from django.contrib import admin
from .models import AppEnvironment, AppName, AppVersion

class AppNameAdmin(admin.ModelAdmin):
    list_display = ('app_name',)
    search_fields = ('app_name',)

admin.site.register(AppName, AppNameAdmin)

class AppEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('env_name',)
    search_fields = ('env_name',)

admin.site.register(AppEnvironment, AppEnvironmentAdmin)

from django.contrib import admin
from django.apps import apps
from django.contrib.sessions.models import Session

# Get the app configuration for the TMS app
tms_app_config = apps.get_app_config('TMS')

# Iterate over all models in the TMS app and register them with the admin site
for model in tms_app_config.get_models():
    admin.site.register(model)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
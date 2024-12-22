from django.contrib import admin
from .models import Report
# Register your models here.

# this registers the Report model with the admin site
admin.site.register(Report)
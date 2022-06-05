from django.contrib import admin

# Register your models here.
from .models import Photo, Style


admin.site.register(Photo)
admin.site.register(Style)

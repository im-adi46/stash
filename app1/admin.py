from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Calculation

admin.site.register(CustomUser)
admin.site.register(Calculation)

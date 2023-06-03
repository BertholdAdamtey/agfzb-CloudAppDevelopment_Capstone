from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel

# @admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
admin.site.register(CarMake)
admin.site.register(CarModel)
# Register models here

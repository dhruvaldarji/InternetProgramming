from django.contrib import admin

# Register your models here.
from .models import Area, Location, Category, Measurement


# Inlines

class LocationInline(admin.TabularInline):
    model = Location


class MeasurementInline(admin.TabularInline):
    model = Measurement


# Model Admins

class AreaModelAdmin(admin.ModelAdmin):
    inlines = [
        LocationInline
    ]


class LocationModelAdmin(admin.ModelAdmin):
    inlines = [
        MeasurementInline
    ]


class CategoryModelAdmin(admin.ModelAdmin):
    filter_horizontal = ("members",)
    pass


# Register Model
admin.site.register(Area, AreaModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Location, LocationModelAdmin)

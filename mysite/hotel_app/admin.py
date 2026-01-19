from functools import lru_cache

from django.contrib import admin
from .models import (UserProfile, Country, City, Hotel, Service, ImageHotel,
                     ImageRoom, Room, Review, BookingHotel)
from modeltranslation.admin import TranslationAdmin

@admin.register(City, Country, Service)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ImageHotelInline(admin.TabularInline):
    model = ImageHotel
    extra = 1

class ImageRoomInline(admin.TabularInline):
    model = ImageRoom
    extra = 1

class AdminRoom(admin.ModelAdmin):
    inlines = [ImageRoomInline]

class AdminHotel(admin.ModelAdmin):
    inlines = [ImageHotelInline]


admin.site.register(UserProfile)
admin.site.register(Hotel, AdminHotel)
admin.site.register(Room, AdminRoom)
admin.site.register(Review)
admin.site.register(BookingHotel)


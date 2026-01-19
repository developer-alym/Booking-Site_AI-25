from .models import Country, City, Service
from modeltranslation.translator import TranslationOptions,register

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name', )

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name', )

@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('service_name', )
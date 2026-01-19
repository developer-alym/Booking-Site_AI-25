from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(70)], default=18)
    phone_number = PhoneNumberField(region='KG', default='+996')
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    USER_ROLE = (
    ('client', 'client'),
    ('owner', 'owner')
    )
    user_role = models.CharField(max_length=10, choices=USER_ROLE, default='client')


class Country(models.Model):
    country_name = models.CharField(max_length=32)
    country_image = models.ImageField(upload_to='country_image')

    def __str__(self):
        return self.country_name

class City(models.Model):
    city_name = models.CharField(max_length=32)
    city_image = models.ImageField(upload_to='city_images')

    def __str__(self):
        return self.city_name


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_images')
    service_name = models.CharField(max_length=32)

    def __str__(self):
        return self.service_name

class Hotel(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='hotel_country')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotel_city')
    hotel_name = models.CharField(max_length=32)
    hotel_image = models.ImageField(upload_to='hotel_images/')
    address = models.CharField(max_length=60)
    service = models.ManyToManyField(Service)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city}: {self.hotel_name}'

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([i.stars for i in reviews]) / reviews.count()
        return 0

    def get_count_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0


class ImageHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images_hotel')
    image = models.ImageField(upload_to='images_hotel')

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_name = models.PositiveSmallIntegerField(default=0)
    room_image = models.ImageField(upload_to='room_images/')
    ROOM_TYPE = (
    ('Семейный', 'Семейный'),
    ('Одноместный', 'Одноместный'),
    ('Двухместный', 'Двухместный'),
    ('Люкс', 'Люкс')
    )
    room_type = models.CharField(max_length=15, choices=ROOM_TYPE)
    ROOM_STATUS = (
    ('Свободень', 'Свободень'),
    ('Забронировань', 'Забронировань')
    )
    room_status = models.CharField(max_length=15, choices=ROOM_STATUS, default='Свободень')
    price = models.PositiveSmallIntegerField(default=0)

class ImageRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_room')


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(null=True, blank=True)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)


class BookingHotel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    grown_ups = models.PositiveSmallIntegerField(default=0)
    children = models.PositiveSmallIntegerField(default=0)








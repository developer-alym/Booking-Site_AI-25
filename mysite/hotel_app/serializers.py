from .models import (UserProfile, Country, City, Hotel, Service, ImageHotel,
                     ImageRoom, Room, Review, BookingHotel)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'profile_image']

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_image']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_image']


class HotelListSerializer(serializers.ModelSerializer):
    city = CityListSerializer()
    get_avg_rating = serializers.SerializerMethodField()
    get_count_rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_image', 'city', 'get_avg_rating', 'get_count_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class ImageHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHotel
        fields = ['id', 'image']


class HotelSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name']


class CityDetailSerializer(serializers.ModelSerializer):
    hotel_city = HotelListSerializer(read_only=True, many=True)

    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image', 'hotel_city']

class CountryDetailSerializer(serializers.ModelSerializer):
    hotel_country = HotelListSerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['id', 'country_name', 'country_image', 'hotel_country']

class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSimpleSerializers()

    class Meta:
        model = Room
        fields = ['id', 'room_name', 'room_image', 'room_type', 'room_status', 'price',
                  'hotel']

class ImageRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRoom
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'stars']

class BookingHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHotel
        fields = '__all__'


class HotelDetailSerializer(serializers.ModelSerializer):
    country = CountryListSerializer()
    city = CityListSerializer()
    service = ServiceSerializer(many=True)
    images_hotel = ImageHotelSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_rating = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_image', 'images_hotel', 'country', 'city', 'get_avg_rating',
                  'get_count_rating',
                  'service', 'address', 'description', 'reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()
        


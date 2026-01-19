from .views import (UserProfileViewSet, CountryDetailViewSet, CountryListViewSet,
                    CityListViewSet, CityDetailViewSet, ServiceViewSet,
                    HotelListViewSet, HotelDetailViewSet, ImagesHotelViewSet, RoomViewSet, ImageRoomViewSet, ReviewViewSet,
                    BookingHotelViewSet, CustomLoginView, RegisterView, LogoutView)
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'user-profile', UserProfileViewSet, basename='user-profile')
router.register(r'service', ServiceViewSet, basename='service')
router.register(r'image-hotel', ImagesHotelViewSet, basename='image-hotel')
router.register(r'room', RoomViewSet, basename='room')
router.register(r'image-room', ImageRoomViewSet, basename='image-room')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'booking-hotel', BookingHotelViewSet, basename='booking-hotel')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('city/', CityListViewSet.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailViewSet.as_view(), name='city-detail'),

    path('country/', CountryListViewSet.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailViewSet.as_view(), name='country-detail'),

    path('hotel/', HotelListViewSet.as_view(), name='hotel-list'),
    path('hotel/<int:pk>/', HotelDetailViewSet.as_view(), name='hotel-detail')
]





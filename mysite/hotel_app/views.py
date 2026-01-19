from rest_framework import viewsets, generics, permissions, status
from .models import (UserProfile, Country, City, Hotel, Service, ImageHotel,
                     ImageRoom, Room, Review, BookingHotel)
from .serializers import (UserProfileSerializer, CountryListSerializer, CountryDetailSerializer,
                          CityListSerializer, CityDetailSerializer, ServiceSerializer,
                          HotelListSerializer, HotelDetailSerializer, ImageHotelSerializer, ImageRoomSerializer, RoomSerializer, ReviewSerializer,
                          BookingHotelSerializer, UserSerializer, LoginSerializer)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import HotelFilter, RoomFilter
from .pagination import HotelPagination, RoomPagination
from .permissions import CheckUserStatus, CheckOwner

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CountryListViewSet(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CountryDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityListViewSet(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CityDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HotelListViewSet(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['hotel_name']
    filterset_class = HotelFilter
    pagination_class = HotelPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUserStatus]

class HotelDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUserStatus, CheckOwner]

class ImagesHotelViewSet(viewsets.ModelViewSet):
    queryset = ImageHotel.objects.all()
    serializer_class = ImageHotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['room_name']
    ordering_fields = ['price']
    filterset_class = RoomFilter
    pagination_class = RoomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ImageRoomViewSet(viewsets.ModelViewSet):
    queryset = ImageRoom.objects.all()
    serializer_class = ImageRoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingHotelViewSet(viewsets.ModelViewSet):
    queryset = BookingHotel.objects.all()
    serializer_class = BookingHotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



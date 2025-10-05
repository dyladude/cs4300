from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings.views import MovieViewSet, SeatViewSet, BookingViewSet, home

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movie')
router.register('seats', SeatViewSet, basename='seat')
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('djadmin/', admin.site.urls),               # admin workaround path
    path('api/', include(router.urls)),              # API only under /api/
    path('api-auth/', include('rest_framework.urls')),# optional DRF login
    path('', home, name='home'),                     # homepage at root
]


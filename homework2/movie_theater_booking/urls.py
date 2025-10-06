from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings.views import (
    MovieViewSet, SeatViewSet, BookingViewSet, movie_list, seat_booking,
     booking_history, signup, CleanLoginView, )
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movie')
router.register('seats', SeatViewSet, basename='seat')
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('djadmin/', admin.site.urls),               # admin workaround path
    path('api/', include(router.urls)),              # REST API
    path('api-auth/', include('rest_framework.urls')),# optional DRF login

    # site pages
    path('', movie_list, name='movie_list'),         # Homepage is movie list
    path('book/<int:movie_id>/', seat_booking, name='book_seat'),
    path('history/', booking_history, name='booking_history'),

    # auth (site)
    path('accounts/login/',  CleanLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', signup, name='signup'),
]


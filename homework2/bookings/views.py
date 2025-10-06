from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Seat, Booking
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Exists, OuterRef
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

def home(request):
    return HttpResponse("Movie app is running ")

def movie_list(request):
    movies = Movie.objects.all().order_by('title')
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = (
        Seat.objects.order_by('seat_number')
        .annotate(is_booked=Exists(
            Booking.objects.filter(movie=movie, seat=OuterRef('pk'))
        ))
    )
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

def booking_history(request):
    bookings = []
    if request.user.is_authenticated:
        bookings = (Booking.objects
                    .filter(user=request.user)
                    .select_related('movie', 'seat')
                    .order_by('-booking_date'))
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)             # auto-login after signup
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def available(self, request):
        qs = self.get_queryset().filter(booking_status=False)
        return Response(SeatSerializer(qs, many=True).data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('movie', 'seat', 'user')
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # limit to current user's bookings
        return self.queryset.filter(user=self.request.user)

    
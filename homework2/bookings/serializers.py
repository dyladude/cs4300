from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(source='movie', queryset=Movie.objects.all(), write_only=True)
    seat_id = serializers.PrimaryKeyRelatedField(source='seat', queryset=Seat.objects.all(), write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date', 'movie_id', 'seat_id']
        read_only_fields = ['user', 'booking_date']

    def create(self, validated_data):
        # attach the logged-in user
        request = self.context['request']
        validated_data['user'] = request.user
        movie = validated_data['movie']
        seat = validated_data['seat']

        # per-movie check
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            raise serializers.ValidationError("That seat is already booked for this movie.")

        return super().create(validated_data)


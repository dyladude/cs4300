from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date

from rest_framework.test import APIClient

from .models import Movie, Seat, Booking

TEST_PASSWORD = "TestPassword123"

User = get_user_model()

API_MOVIES   = "/api/movies/"
API_SEATS    = "/api/seats/"
API_AVAILABLE= "/api/seats/available/"
API_BOOKINGS = "/api/bookings/"

# -----------------------
# Unit tests: Models
# -----------------------
class ModelTests(TestCase):
    def test_create_movie(self):
        m = Movie.objects.create(
            title="Car!",
            description="Vroom",
            release_date=date(2024, 1, 1),
            duration=90,
        )
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(m.title, "Car!")
        self.assertEqual(m.duration, 90)

    def test_seat_defaults_to_not_booked(self):
        s = Seat.objects.create(seat_number="A1")
        self.assertFalse(s.booking_status)

    def test_booking_relations(self):
        user = User.objects.create_user(username="u1", password="p")
        m = Movie.objects.create(title="Boat!", description="", release_date=date(2024,1,2), duration=95)
        s = Seat.objects.create(seat_number="B4")
        b = Booking.objects.create(movie=m, seat=s, user=user)
        self.assertEqual(b.movie, m)
        self.assertEqual(b.seat, s)
        self.assertEqual(b.user, user)

# -----------------------
# Integration tests: API
# -----------------------
class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user("alice", password="TEST_PASSWORD")
        self.user2 = User.objects.create_user("bob", password="TEST_PASSWORD")
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="desc",
            release_date=date(2024, 1, 3),
            duration=100,
        )
        # two seats: A1, A2
        self.s1 = Seat.objects.create(seat_number="A1")  # available
        self.s2 = Seat.objects.create(seat_number="A2")  # we'll mark as booked

    def test_movies_list_is_public(self):
        # /api/movies/ should exist (CRUD endpoint) and be GET-able
        r = self.client.get(API_MOVIES)
        self.assertEqual(r.status_code, 200)

    def test_available_seats_filters_out_booked(self):
        # mark A2 as booked (global flag used by your code)
        self.s2.booking_status = True
        self.s2.save()

        r = self.client.get(API_AVAILABLE)
        self.assertEqual(r.status_code, 200)
        ids = [item["id"] for item in r.json()]
        self.assertIn(self.s1.id, ids)
        self.assertNotIn(self.s2.id, ids)

    def test_booking_requires_auth(self):
        payload = {"movie_id": self.movie.id, "seat_id": self.s1.id}
        r = self.client.post(API_BOOKINGS, payload, format="json")
        # DRF's IsAuthenticated → 403 for anonymous
        self.assertIn(r.status_code, (401, 403))

    def test_user_can_book_and_seat_becomes_unavailable(self):
        payload = {"movie_id": self.movie.id, "seat_id": self.s1.id}

        # Authenticate this client for the request (bypasses any backend/CSRF quirks)
        self.client.force_authenticate(user=self.user1)

        r = self.client.post(API_BOOKINGS, payload, format="json")
        self.assertEqual(r.status_code, 201, msg=r.content)

        # back to anonymous for subsequent calls (optional, but tidy)
        self.client.force_authenticate(user=None)

        # per-movie availability check
        r2 = self.client.get(f"{API_AVAILABLE}?movie={self.movie.id}")
        self.assertEqual(r2.status_code, 200, msg=r2.content)
        ids = [item["id"] for item in r2.json()]
        self.assertNotIn(self.s1.id, ids)

        # user sees their booking (re-auth so this list is for alice)
        self.client.force_authenticate(user=self.user1)
        r3 = self.client.get(API_BOOKINGS)
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(len(r3.json()), 1)
        self.client.force_authenticate(user=None)


    def test_cannot_double_book_same_seat(self):
        # first booking by alice
        self.client.login(username="alice", password="TEST_PASSWORD")
        r1 = self.client.post(API_BOOKINGS, {"movie_id": self.movie.id, "seat_id": self.s1.id}, format="json")
        self.assertEqual(r1.status_code, 201, msg=r1.content)
        self.client.logout()

        # second attempt (same seat) by bob should fail because seat.booking_status=True
        self.client.login(username="bob", password="TEST_PASSWORD")
        r2 = self.client.post(API_BOOKINGS, {"movie_id": self.movie.id, "seat_id": self.s1.id}, format="json")
        self.assertEqual(r2.status_code, 400, msg=r2.content)

    def test_user_sees_only_own_bookings(self):
        # alice books one seat
        self.client.login(username="alice", password="TEST_PASSWORD")
        self.client.post(API_BOOKINGS, {"movie_id": self.movie.id, "seat_id": self.s1.id}, format="json")
        self.client.logout()

        # bob should see none
        self.client.login(username="bob", password="TEST_PASSWORD")
        r = self.client.get(API_BOOKINGS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), [])

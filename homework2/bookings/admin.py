from django.contrib import admin, messages
from django.conf import settings
from .models import Movie, Seat, Booking

# Admin chrome
admin.site.site_header = "Movie Theater Admin"
admin.site.site_title = "Movie Theater Admin"
admin.site.index_title = "Dashboard"

# Make "View site" / home links use the correct root (handles DevEdu proxy)
prefix = (getattr(settings, "FORCE_SCRIPT_NAME", "") or "").rstrip("/")
admin.site.site_url = (prefix + "/") if prefix else "/"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration")
    search_fields = ("title",)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "booking_status")
    search_fields = ("seat_number",)
    actions = ["generate_standard_seats"]

    def generate_standard_seats(self, request, queryset):
        """
        Create rows A–C with 10 seats each (A1–C10).
        Safe to run multiple times; existing seats are skipped.
        """
        rows = "ABC"
        per_row = 10
        created = 0
        skipped = 0

        for r in rows:
            for i in range(1, per_row + 1):
                _, was_created = Seat.objects.get_or_create(seat_number=f"{r}{i}")
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.message_user(
            request,
            f"Generated seats A1–C10 → created {created}, skipped {skipped} existing.",
            level=messages.SUCCESS,
        )
    generate_standard_seats.short_description = "Generate seats A1–C10"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("movie", "seat", "user", "created_at")
    search_fields = ("movie__title", "seat__seat_number", "user__username")
    list_filter = ("movie",)

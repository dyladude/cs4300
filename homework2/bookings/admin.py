from django.contrib import admin
from .models import Movie, Seat, Booking
from django.conf import settings

# Register your models here.

admin.site.register(Movie)
admin.site.register(Seat)
admin.site.register(Booking)

admin.site.site_header = "Movie Theater Admin"
admin.site.site_title = "Movie Theater Admin"
admin.site.index_title = "Dashboard"

# So "View site" / home links go to just 1 prefixed root
prefix = (getattr(settings, "FORCE_SCRIPT_NAME", "") or "").rstrip("/")
admin.site.site_url = (prefix + "/") if prefix else "/"
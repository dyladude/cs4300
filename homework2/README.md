# Movie Theater Booking (HW2)

Django + DRF app to list movies, view seats, and book seats **per movie**.  
Bootstrap UI, styled admin, login/signup, and a REST API.  
Deployed on **Render**; also runnable in **DevEdu** (proxied) for grading.

---

## Project Links

- **Live (Render):** https://cs4300-dylan-trent-homework-2.onrender.com/
- **GitHub Repo:** https://github.com/dyladude/cs4300 (app lives in `homework2/`)

> On Render, set the service **Root Directory** to `homework2`.

---

## Project Structure

```
homework2/
  manage.py
  requirements.txt
  movie_theater_booking/
    settings.py
    urls.py
    middleware.py
    wsgi.py
  bookings/
    models.py
    views.py
    serializers.py
    admin.py
    tests.py
  templates/
    bookings/...
    admin/...
    registration/...
  staticfiles/        # populated by collectstatic in production
```

Key points:
- **Per-movie availability**: `Booking` is unique on `(movie, seat)`—same seat can be used across movies, but only once per movie.
- **Proxy-safe URLs**: in DevEdu we conditionally enable `FORCE_SCRIPT_NAME="/proxy/3000"` via `DEVEDU=1`; on Render, **no** prefix.
- **Clean redirects**: `CleanLoginView` + `FixProxyRedirectMiddleware` prevent double `/proxy/3000` in DevEdu redirects.

---

## Running Locally (DevEdu / Grading)

```bash
# 1) Create venv
python3 -m venv hw2venv --system-site-packages
source hw2venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Migrate & create admin
python manage.py migrate
python manage.py createsuperuser

# 4) Run with the DevEdu proxy prefix
export DEVEDU=1
python manage.py runserver 0.0.0.0:3000
```

Open: `https://editor-<your-container>.devedu.io/proxy/3000/`

---

## Deployment (Render)

**Root Directory:** `homework2`

**Environment variables**
- `SECRET_KEY` = (long random string)
- `DEBUG` = `False`
- Optional: `DATABASE_URL` (Render Postgres). If omitted, SQLite is used.

**Build Command**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command** (runs migrations each boot; creates a superuser once if env vars present)
```bash
python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn --bind 0.0.0.0:$PORT movie_theater_booking.wsgi:application
```

**Auto-superuser (optional, first deploy)**  
Set:
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

> On Render, do **not** set `DEVEDU`. The proxy prefix is only for DevEdu.

---

## URLs

### Site (DevEdu)
- Home: `/proxy/3000/`
- Seat selection: `/proxy/3000/book/<movie_id>/`
- Booking history: `/proxy/3000/history/`
- Auth: `/proxy/3000/accounts/login|logout|signup/`
- Admin: `/proxy/3000/djadmin/`

### Site (Render)
- Home: `/`
- Seat selection: `/book/<movie_id>/`
- Booking history: `/history/`
- Auth: `/accounts/login|logout|signup/`
- Admin: `/djadmin/`

### API (both)
- `GET /api/movies/`
- `GET /api/seats/available/?movie=<movie_id>`
- `GET|POST /api/bookings/`
  - `POST` JSON: `{"movie_id": <id>, "seat_id": <id>}`

---

## Tests

Location: `bookings/tests.py` (models + API: auth, availability, double-booking, user scoping).

Run:
```bash
python manage.py test bookings -v 2
```

You should see **9 tests** passing.

---

## Notes / Decisions

- **Per-movie availability** implemented via query `?movie=<id>` in `/api/seats/available/`.
- **Proxy quirks (DevEdu)** handled by:
  - prefix-less `next` values (e.g., `/`, `/djadmin/`),
  - `CleanLoginView` and `FixProxyRedirectMiddleware` (safe no-ops on Render).
- **Static files** served by WhiteNoise in production.

---

## Submission Checklist

- [ ] Zip for Canvas contains:
  - Source code (incl. templates, middleware, static),
  - `bookings/tests.py`,
  - This **README.md**.
- [ ] Frequent commits pushed to GitHub.
- [ ] DevEdu copy runnable (`DEVEDU=1`, `runserver 0.0.0.0:3000`).
- [ ] Render deployment live and reachable: https://cs4300-dylan-trent-homework-2.onrender.com/
  - Build/Start commands set,
  - Migrations run at boot,
  - Admin superuser created,
  - App responds at public URL.
- [ ] Tests: `python manage.py test bookings -v 2` → **OK**.

---

## AI Usage Disclosure (Required)

I used **GPT-5 Thinking (ChatGPT)** to assist with:
- Diagnosing DevEdu proxy redirect issues and drafting the `CleanLoginView` + `FixProxyRedirectMiddleware`.
- Writing/refining templates & JS for the seat booking flow (login redirect on 403).
- Drafting and adapting unit/integration tests in `bookings/tests.py` (including per-movie availability and password validator updates).
- Preparing Render deployment settings (WhiteNoise, `dj-database-url`, commands), and this README.

All AI-generated content was **reviewed, tested, and edited** by me; final code and configuration choices are mine.

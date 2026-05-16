# Lumina Books

A modern AI-powered online book store built with Django, SQLite, Tailwind CDN, and a polished glassmorphism interface.

## Features

- Landing page, book catalog, book detail pages, auth, checkout, cart drawer, and staff dashboard
- Django ORM models for books, categories, newsletter subscribers, orders, and order items
- Gemini API integration for spoiler-free AI book summaries
- Responsive dark glass UI with accessible focus states, skip links, reduced-motion support, skeleton loading cards, and smooth reveal animations
- Secure Django admin mounted at `/secure-admin/`

## Setup

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

AI summaries are powered by Gemini through a private local `.env` file. The real `.env` file is intentionally ignored by Git so credentials are never committed.

```env
GEMINI_API_KEY=
```

Open `http://127.0.0.1:8000/`.

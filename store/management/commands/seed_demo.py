from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Book, Category


BOOKS = [
    ("AI & Future", "The Alignment Age", "Mira Voss", "A field guide to building humane AI systems with clarity, taste, and durable governance.", "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=800&q=80", True, True),
    ("Design", "Interfaces That Breathe", "Noah Vale", "A practical meditation on product surfaces, motion, hierarchy, and the emotional shape of software.", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=800&q=80", True, False),
    ("Strategy", "Monopoly of Meaning", "Elena Park", "How category-defining companies turn sharp positioning into a compounding product advantage.", "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=800&q=80", False, True),
    ("Science", "Dark Matter Mornings", "Ishan Rao", "A lyrical tour through cosmology, uncertainty, and the instruments that help us see the invisible.", "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=800&q=80", True, False),
    ("Fiction", "The Last Archive", "June Calder", "A cinematic novel about memory, encrypted cities, and a librarian racing a vanishing signal.", "https://images.unsplash.com/photo-1519682337058-a94d519337bc?auto=format&fit=crop&w=800&q=80", False, True),
    ("Business", "Operator Mode", "Cassian Reed", "A calm, exacting playbook for teams that want faster decisions without losing craft.", "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&w=800&q=80", True, True),
]


class Command(BaseCommand):
    help = "Seed demo categories and books."

    def handle(self, *args, **options):
        for index, (category_name, title, author, description, cover_url, best, new) in enumerate(BOOKS, start=1):
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"description": f"Curated {category_name.lower()} titles for ambitious readers."},
            )
            Book.objects.get_or_create(
                title=title,
                author=author,
                defaults={
                    "category": category,
                    "description": description,
                    "cover_url": cover_url,
                    "price": Decimal("18.00") + index,
                    "stock": 12 + index,
                    "rating": Decimal("4.50") + Decimal(index) / Decimal("100"),
                    "is_best_seller": best,
                    "is_new_arrival": new,
                },
            )
        self.stdout.write(self.style.SUCCESS("Demo bookstore data is ready."))

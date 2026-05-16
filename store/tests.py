from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Book, Category, NewsletterSubscriber


class StoreViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="AI")
        self.book = Book.objects.create(
            category=self.category,
            title="Practical Intelligence",
            author="Ada Stone",
            description="A useful book about AI products.",
            price=Decimal("19.00"),
            stock=8,
            is_best_seller=True,
            is_new_arrival=True,
        )

    def test_catalog_and_detail_pages_render(self):
        catalog = self.client.get(reverse("store:book_list"))
        detail = self.client.get(self.book.get_absolute_url())

        self.assertContains(catalog, "Practical Intelligence")
        self.assertContains(detail, "Gemini summary")

    def test_cart_add_and_checkout_redirect_when_empty(self):
        response = self.client.post(reverse("store:add_cart", args=[self.book.id]), {"next": reverse("store:book_list")})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["bookstore_cart"][str(self.book.id)], 1)

        session = self.client.session
        session["bookstore_cart"] = {}
        session.save()
        checkout = self.client.get(reverse("store:checkout"))
        self.assertEqual(checkout.status_code, 302)

    def test_newsletter_subscription(self):
        response = self.client.post(reverse("store:newsletter"), {"email": "reader@example.com"})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsletterSubscriber.objects.filter(email="reader@example.com").exists())

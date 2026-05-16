from .cart import cart_items
from .forms import NewsletterForm
from .models import Book, Category


def cart_context(request):
    items, total, count = cart_items(request.session)
    return {
        "cart_items": items,
        "cart_total": total,
        "cart_count": count,
        "nav_categories": Category.objects.all()[:8],
        "newsletter_form": NewsletterForm(),
        "cart_suggestions": Book.objects.order_by("-rating")[:3],
    }

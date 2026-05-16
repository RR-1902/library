from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import add_to_cart, cart_items, clear_cart, remove_from_cart
from .forms import CheckoutForm, NewsletterForm, RegisterForm
from .models import Book, Category, NewsletterSubscriber, Order, OrderItem
from .services import generate_book_summary


def landing(request):
    all_books = Book.objects.select_related("category")
    best_sellers = all_books.filter(is_best_seller=True)[:6]
    new_arrivals = all_books.filter(is_new_arrival=True)[:6]
    featured = Book.objects.select_related("category").first()
    ai_picks = all_books.filter(rating__gte=4.5)[:4]
    trending = all_books.order_by("-rating", "-created_at")[:8]
    collections = [
        {"name": "Mind Expansion", "tone": "Philosophy, psychology, and science titles for bigger mental models."},
        {"name": "Future of AI", "tone": "Practical intelligence, alignment, automation, and tomorrow's systems."},
        {"name": "Startup Essentials", "tone": "Operator-grade books on positioning, strategy, and product velocity."},
    ]
    return render(
        request,
        "store/landing.html",
        {
            "best_sellers": best_sellers,
            "new_arrivals": new_arrivals,
            "featured": featured,
            "ai_picks": ai_picks,
            "trending": trending,
            "collections": collections,
        },
    )


def book_list(request):
    books = Book.objects.select_related("category")
    categories = Category.objects.annotate(book_count=Count("books"))
    active_category = request.GET.get("category")
    query = request.GET.get("q", "").strip()
    min_rating = request.GET.get("rating")
    max_price = request.GET.get("price")
    author = request.GET.get("author", "").strip()
    year = request.GET.get("year", "").strip()
    active_flags = {
        "best": request.GET.get("best") == "1",
        "new": request.GET.get("new") == "1",
        "ai": request.GET.get("ai") == "1",
        "stock": request.GET.get("stock") == "1",
    }
    if active_category:
        books = books.filter(category__slug=active_category)
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    if min_rating:
        books = books.filter(rating__gte=min_rating)
    if max_price:
        books = books.filter(price__lte=max_price)
    if author:
        books = books.filter(author__icontains=author)
    if active_flags["best"]:
        books = books.filter(is_best_seller=True)
    if active_flags["new"]:
        books = books.filter(is_new_arrival=True)
    if active_flags["ai"]:
        books = books.filter(rating__gte=4.5)
    if active_flags["stock"]:
        books = books.filter(stock__gt=0)
    active_filter_count = sum(
        [
            bool(active_category),
            bool(query),
            bool(min_rating),
            bool(max_price),
            bool(author),
            bool(year),
            *active_flags.values(),
        ]
    )
    return render(
        request,
        "store/book_list.html",
        {
            "books": books,
            "categories": categories,
            "active_category": active_category,
            "query": query,
            "min_rating": min_rating,
            "max_price": max_price,
            "author": author,
            "year": year,
            "active_flags": active_flags,
            "active_filter_count": active_filter_count,
            "suggested_books": Book.objects.order_by("-rating")[:3],
        },
    )


def book_detail(request, slug):
    book = get_object_or_404(Book.objects.select_related("category"), slug=slug)
    if not book.ai_summary:
        summary = generate_book_summary(book)
        if summary:
            book.ai_summary = summary
            book.save(update_fields=["ai_summary"])
    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    return render(request, "store/book_detail.html", {"book": book, "related": related})


@require_POST
def add_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    add_to_cart(request.session, book.id)
    messages.success(request, f"{book.title} added to your cart.")
    return redirect(request.POST.get("next") or book.get_absolute_url())


@require_POST
def remove_cart(request, book_id):
    remove_from_cart(request.session, book_id)
    messages.info(request, "Book removed from cart.")
    return redirect(request.POST.get("next") or "store:book_list")


def checkout(request):
    items, total, count = cart_items(request.session)
    if not items:
        messages.info(request, "Your cart is ready when you are.")
        return redirect("store:book_list")
    form = CheckoutForm(request.POST or None, initial={"email": getattr(request.user, "email", "")})
    if request.method == "POST" and form.is_valid():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=form.cleaned_data["email"],
            full_name=form.cleaned_data["full_name"],
            total=total,
        )
        OrderItem.objects.bulk_create(
            [OrderItem(order=order, book=row["book"], quantity=row["quantity"], price=row["book"].price) for row in items]
        )
        clear_cart(request.session)
        messages.success(request, "Checkout complete. Your reading stack is reserved.")
        return redirect("store:landing")
    return render(request, "store/checkout.html", {"form": form, "items": items, "total": total, "count": count})


@require_POST
def newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        NewsletterSubscriber.objects.get_or_create(email=form.cleaned_data["email"])
        messages.success(request, "You are on the list.")
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(request.POST.get("next") or "store:landing")


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to Lumina Books.")
        return redirect("store:landing")
    return render(request, "store/register.html", {"form": form})


@staff_member_required(login_url="store:login")
def admin_dashboard(request):
    stats = {
        "books": Book.objects.count(),
        "categories": Category.objects.count(),
        "orders": Order.objects.count(),
        "subscribers": NewsletterSubscriber.objects.count(),
        "revenue": Order.objects.aggregate(total=Sum("total"))["total"] or 0,
    }
    recent_orders = Order.objects.prefetch_related("items")[:6]
    low_stock = Book.objects.filter(stock__lte=5)[:6]
    category_stats = Category.objects.annotate(book_count=Count("books")).order_by("-book_count")[:5]
    return render(
        request,
        "store/admin_dashboard.html",
        {
            "stats": stats,
            "recent_orders": recent_orders,
            "low_stock": low_stock,
            "category_stats": category_stats,
            "top_books": Book.objects.order_by("-rating")[:5],
        },
    )

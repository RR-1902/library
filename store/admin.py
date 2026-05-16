from django.contrib import admin

from .models import Book, Category, NewsletterSubscriber, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "price", "stock", "is_best_seller", "is_new_arrival")
    list_filter = ("category", "is_best_seller", "is_new_arrival")
    prepopulated_fields = {"slug": ("title", "author")}
    search_fields = ("title", "author", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "total", "created_at")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)
    search_fields = ("full_name", "email")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)

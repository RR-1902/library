from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("books/", views.book_list, name="book_list"),
    path("books/<slug:slug>/", views.book_detail, name="book_detail"),
    path("cart/add/<int:book_id>/", views.add_cart, name="add_cart"),
    path("cart/remove/<int:book_id>/", views.remove_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="store/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("studio/", views.admin_dashboard, name="admin_dashboard"),
]

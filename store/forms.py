from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import NewsletterSubscriber


class GlassInputMixin:
    field_classes = "glass-input"

    def _style_fields(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", self.field_classes)


class RegisterForm(GlassInputMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class CheckoutForm(GlassInputMixin, forms.Form):
    full_name = forms.CharField(max_length=140)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={"class": "newsletter-input", "placeholder": "you@example.com"})
        }

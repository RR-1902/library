from django.conf import settings


def generate_book_summary(book):
    if not settings.GEMINI_API_KEY:
        return ""

    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        prompt = (
            "Write a polished, spoiler-free, accessible bookstore summary in 90 words. "
            f"Title: {book.title}. Author: {book.author}. Description: {book.description}"
        )
        response = model.generate_content(prompt)
        return (response.text or "").strip()
    except Exception:
        return ""

from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse

def url_for(endpoint, **values):
    """
    Flask-compatible url_for helper for Jinja2 templates in Django.
    """
    if endpoint == 'static':
        filename = values.get('filename', '')
        return static(filename)
    elif endpoint in ('render_page', 'page_view'):
        page_name = values.get('page_name', 'index.html')
        if not page_name:
            return "/"
        return f"/{page_name}"
    try:
        return reverse(endpoint, kwargs=values)
    except Exception:
        page_name = values.get('page_name', '')
        return f"/{page_name}" if page_name else "/"

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'url_for': url_for,
    })
    return env

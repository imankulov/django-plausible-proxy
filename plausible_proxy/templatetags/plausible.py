from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def plausible(domain=settings.PLAUSIBLE_DOMAIN, script="script.js"):
    """Return a script tag referencing the script.js."""
    attrs = {
        "defer": True,
        "data-domain": domain,
        "src": reverse("plausible:script-proxy", args=(script,)),
    }
    return mark_safe(f"<script{flatatt(attrs)}></script>")

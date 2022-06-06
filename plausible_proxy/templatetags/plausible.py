from django import template
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils.safestring import mark_safe

from plausible_proxy.services import get_default_domain

register = template.Library()


@register.simple_tag(takes_context=True)
def plausible(context, domain=None, script="script.js"):
    """Return a script tag referencing the script.js.

    Args:
        context: Template context.
        domain: The value to include in the `<script data-domain="..."`. If not
            set, the value is taken from PLAUSIBLE_DOMAIN. If PLAUSIBLE_DOMAIN is
            not defined, the value is taken from the request.
        script: the script name without path or domain name. The value to include in
            the `<script src="...">`

    Returns:
        The script tag to include in the base template. E.g.,
        `<script data-domain="example.com" src="/js/script.js" defer></script>`
    """
    if domain is None:
        domain = get_default_domain(context["request"])
    attrs = {
        "defer": True,
        "data-domain": domain,
        "src": reverse("plausible:script-proxy", args=(script,)),
    }
    return mark_safe(f"<script{flatatt(attrs)}></script>")

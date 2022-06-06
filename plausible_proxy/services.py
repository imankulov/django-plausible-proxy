from typing import Any, Dict, Optional, Tuple

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest

# Ref: https://plausible.io/docs/script-extensions
ALLOWED_SCRIPT_NAMES = {
    "script.js",
    "script.hash.js",
    "script.outbound-links.js",
    "script.file-downloads.js",
    "script.exclusions.js",
    "script.compat.js",
    "script.local.js",
    "script.manual.js",
}


CACHE_TTL = 86400


SCRIPT_HEADERS = {
    "cache-control": f"public, must-revalidate, max-age={CACHE_TTL}",
    "content-type": "application/javascript",
}

EVENT_HEADERS = {
    "content-type": "text/plain; charset=utf-8",
    "cache-control": "must-revalidate, max-age=0, private",
}

ContentAndHeaders = Tuple[bytes, Dict[str, str]]


def get_script(script_name: str) -> ContentAndHeaders:
    """Return the script by its name.

    Args:
        script_name: the name of the script to download. E.g., `script.js`

    Raises:
        requests.HTTPError if script can't be downloaded.
        ValueError if script_name is invalid.

    Returns:
        The contents of the script as bytes (not a string) and headers to be passed
        back to the response.
    """
    if script_name not in ALLOWED_SCRIPT_NAMES:
        raise ValueError(f"Unknown script {script_name}")

    cache_key = f"plausible:script:{script_name}"
    sentinel = object()

    script_bytes = cache.get(cache_key, sentinel)
    if script_bytes is not sentinel:
        return script_bytes, SCRIPT_HEADERS

    resp = requests.get(f"{get_plausible_base_url()}/js/{script_name}")
    resp.raise_for_status()
    script_bytes = resp.content
    cache.set(cache_key, script_bytes, CACHE_TTL)
    return script_bytes, SCRIPT_HEADERS


def send_custom_event(
    request: HttpRequest,
    name: str,
    domain: Optional[str] = None,
    url: Optional[str] = None,
    referrer: Optional[str] = None,
    screen_width: Optional[int] = None,
    props: Optional[Dict[str, Any]] = None,
) -> bool:
    """Send a custom event to Plausible and return successful status.

    Ref: https://plausible.io/docs/events-api

    Args:
        request: Original Django HTTP request. Will be used to create X-Forwarded-For
            and User-Agent headers.
        domain: Domain name of the site in Plausible. The value from
            settings.PLAUSIBLE_DOMAIN is used by default.
        name: Name of the event. Can specify `pageview` which is a special type of
            event in Plausible. All other names will be treated as custom events.
        url: URL of the page where the event was triggered. If the URL
            contains UTM parameters, they will be extracted and stored. If URL is not
            set, will be extracted from the request.
        referrer: Referrer for this event.
        screen_width: Width of the screen.
        props: Custom properties for the event. See:
            https://plausible.io/docs/custom-event-goals#using-custom-props

    Returns:
        True if request was accepted successfully.
    """
    if url is None:
        url = request.build_absolute_uri()
    if domain is None:
        domain = get_default_domain(request)

    event_data = {
        "name": name,
        "domain": domain,
        "url": url,
        "referrer": referrer,
        "screen_width": screen_width,
        "props": props,
    }
    event_data = {k: v for k, v in event_data.items() if v is not None}

    resp = requests.post(
        get_plausible_event_api_endpoint(),
        json=event_data,
        headers={
            "content-type": "application/json",
            "x-forwarded-for": get_xff(request),
            "user-agent": get_user_agent(request),
        },
    )
    return resp.ok


def get_xff(request: HttpRequest) -> str:
    """Extract and update X-Forwarded-For from the request."""
    remote_addr = request.META["REMOTE_ADDR"]
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return f"{xff}, {remote_addr}"
    return remote_addr


def get_user_agent(request: HttpRequest) -> str:
    """Extract User-Agent header from the request."""
    return request.META.get("HTTP_USER_AGENT") or ""


def get_default_domain(request: HttpRequest) -> str:
    """Return default Plausible domain for send_custom_event().

    The value is taken from settings.PLAUSIBLE_DOMAIN
    """
    return getattr(settings, "PLAUSIBLE_DOMAIN", request.get_host())


def get_plausible_base_url() -> str:
    """Return the Plausible base URL.

    The variable defines the destination to send events. Default to
    https://plausible.io, but you can set a custom value in PLAUSIBLE_BASE_URL if you
    want to send events to your local Plausible installation.
    """
    return getattr(settings, "PLAUSIBLE_BASE_URL", "https://plausible.io")


def get_plausible_event_api_endpoint() -> str:
    return f"{get_plausible_base_url()}/api/event"

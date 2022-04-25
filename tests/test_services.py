"""Tests for `plausible_proxy` package."""

import pytest

from plausible_proxy import send_custom_event
from plausible_proxy.services import get_script, get_xff


def test_get_script_returns_javascript():
    resp, headers = get_script("script.js")
    assert resp.startswith(b"!function()")
    assert headers["content-type"] == "application/javascript"


def test_get_script_raises_exception_on_invalid_filename():
    with pytest.raises(ValueError):
        get_script("xxx.js")


def test_get_xff_without_proxy(rf):
    request = rf.get("/api/event", REMOTE_ADDR="1.2.3.4")
    assert get_xff(request) == "1.2.3.4"


def test_get_xff_with_proxy(rf):
    request = rf.get(
        "/api/event", REMOTE_ADDR="1.2.3.4", HTTP_X_FORWARDED_FOR="1.1.1.1, 2.2.2.2"
    )
    assert get_xff(request) == "1.1.1.1, 2.2.2.2, 1.2.3.4"


def test_send_custom_event_returns_true_on_success(rf):
    request = rf.get("/register", REMOTE_ADDR="1.2.3.4")
    send_custom_event(
        request, "Register", domain="example.com", props={"Plan": "premium"}
    )

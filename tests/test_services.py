"""Tests for `plausible_proxy` package."""

from unittest.mock import patch

import pytest

from plausible_proxy import send_custom_event
from plausible_proxy.services import get_script, get_xff


@pytest.fixture()
def mock_requests():
    with patch("plausible_proxy.services.requests") as requests:
        requests.post.return_value.ok = True
        yield requests


@pytest.mark.parametrize(
    "script_name", ["script.js", "script.hash.js", "script.hash.outbound-links.js"]
)
def test_get_script_returns_javascript(script_name):
    resp, headers = get_script(script_name)
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


def test_send_custom_event_returns_true_on_success(rf, mock_requests):
    request = rf.get("/register", REMOTE_ADDR="1.2.3.4")
    status = send_custom_event(
        request, "Register", domain="example.com", props={"Plan": "premium"}
    )
    assert status is True


def test_send_custom_event_successful_without_domain(rf, mock_requests):
    request = rf.get("/register", REMOTE_ADDR="1.2.3.4", SERVER_NAME="example.com")
    status = send_custom_event(request, "Register", props={"Plan": "premium"})
    assert status is True


def test_send_custom_events_respects_explicit_remote_addr(rf, mock_requests):
    request = rf.get("/register", REMOTE_ADDR="1.2.3.4", SERVER_NAME="example.com")
    status = send_custom_event(
        request, "Register", domain="example.com", remote_addr="1.2.3.5"
    )
    assert status is True

    headers = mock_requests.post.call_args.kwargs["headers"]
    assert headers["x-forwarded-for"] == "1.2.3.5"

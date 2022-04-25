from plausible_proxy.views import event_proxy, script_proxy


def test_script_proxy_proxies_request(rf):
    request = rf.get("/js/script.js")
    resp = script_proxy(request, "script.js")
    assert resp.content.startswith(b"!function()")
    assert resp.status_code == 200


def test_event_proxy_proxies_request(rf):
    event = {
        "n": "pageview",
        "u": "https://example.com/",
        "d": "example.com",
        "r": None,
        "w": 123,
    }
    request = rf.post("/api/event", data=event, content_type="application/json")
    resp = event_proxy(request)
    assert resp.content == b"ok"
    assert resp.status_code == 202

# Django Plausible Proxy

Django application to proxy requests and send server-side events to Plausible Analytics. Plays well with self-hosted and the managed cloud service.

## Proxying

Proxying allows a project owner concerned about missing data seeing a more complete picture. See [Adblockers and using a proxy for analytics](https://plausible.io/docs/proxy/introduction) for the detailed outline of the problem and solution.

When installed and configured in `settings.py` and `urls.py`, the app proxies the HTTP requests as such:

```
https://<yourdomain.com>/js/script.js -> https://plausible.io/js/script.js
https://<yourdomain.com>/api/event    -> https://plausible.io/api/event
```

## Server-side events

Track on the server side events that can't be tracked otherwise, such as API requests.

```python
from plausible_proxy import send_custom_event
...
send_custom_event(request, name="Register", props={"plan": "Premium"})
```

## Installation

Install the package from PyPI.

```shell
pip install django-plausible-proxy
```

Configure Django setting in the `settings.py`.

```python

# Register the app to enable {% plausble %} templatetag.
INSTALLED_APPS = [
    # ...
    "plausible_proxy"
    # ...
]

# Optionally, define a default value for Plausible domain to provide a default value
# for the Plausible domain and the `send_custom_event()` function.
PLAUSIBLE_DOMAIN = "yourdomain.com"

# Optionally, define the plausible endpoint that you would like to post to.
# This is useful if you are self-hosting plausible.
PLAUSIBLE_BASE_URL = "https://plausible.io"

# Optionally, define the value for the script prefix. The default value is "js". When
# you include the script to the page with the {% plausible %} templatetag, it becomes
# available as "<script src='${PLAUSIBLE_SCRIPT_PREFIX}/script.js'></script>". E.g.,
# "<script src='js/script.js'></script>"
#
# Overriding PLAUSIBLE_SCRIPT_PREFIX is helpful to avoid clashes with another script
# of your site that may become available under the same name.

PLAUSIBLE_SCRIPT_PREFIX = "plsbl/js"
```

Update `urls.py`.


```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("", include("plausible_proxy.urls")),
    # ...
]
```

Update your base HTML template to include the plausible templatetag.

```html
{% load plausible %}
<html>
  <head>
      ...
      {% plausible script='script.js' %}
  </head>
```

## API reference


### **`{% plausible %}`**

A templatetag to include the Plausible analytics script to the page.

Arguments:

- `domain` (default to `settings.PLAUSIBLE_DOMAIN`): defines the `data-domain` parameter, the is the domain for the Plausible analytics.
- `script` (default to `script.js`): defines the Plausible script to use. See [Script extensions for enhanced measurement](https://plausible.io/docs/script-extensions) for the list of alternative script names and what they can track for you.

Usage example:

```html
{% load plausible %}
<html>
  <head>
      ...
      {% plausible domain='example.com' script='script.outbound-links.js' %}
  </head>
```

### `plausible_proxy.services.`**`send_custom_event()`**

end a custom event to Plausible and return successful status.

See [Plausible events API](https://plausible.io/docs/events-api) for more information

Arguments:

- `request` (HttpRequest): Original Django HTTP request. Will be used to create X-Forwarded-For and User-Agent headers.
- `name` (string): Name of the event. Can specify `pageview` which is a special type of event in Plausible. All other names will be treated as custom events.
- `domain` (optional string): Domain name of the site in Plausible. The value from settings.PLAUSIBLE_DOMAIN is used by default.
- `url` (optional string): URL of the page where the event was triggered. If not provided, the function extracts the URL from the request. If the URL contains UTM parameters, they will be extracted and stored. If URL is not set, will be extracted from the request.
- `referrer` (optional string): Referrer for this event.
- `screen_width` (optional integer): Width of the screen.
- `props` (optional dict): Custom properties for the event. See: [Using custom props](https://plausible.io/docs/custom-event-goals#using-custom-props).

Returns: True if request was accepted successfully.

Example:

```python
def vote(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    send_custom_event(request, 'vote', props={"candidate": candidate.full_name})
    ...
```

## Contributors

<a href="https://github.com/imankulov/django-plausible-proxy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=imankulov/django-plausible-proxy" />
</a>

import requests
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.views.decorators.csrf import csrf_exempt

from plausible_proxy.services import (
    EVENT_HEADERS,
    PLAUSIBLE_EVENT_API_ENDPOINT,
    get_script,
    get_user_agent,
    get_xff,
)


def script_proxy(request: HttpRequest, script_name: str):
    try:
        script_bytes, script_headers = get_script(script_name)
    except ValueError:
        return HttpResponseNotFound("Not Found")
    except requests.HTTPError:
        return HttpResponseServerError("Internal Server Error")
    return HttpResponse(content=script_bytes, headers=script_headers)


@csrf_exempt
def event_proxy(request: HttpRequest):
    resp = requests.post(
        PLAUSIBLE_EVENT_API_ENDPOINT,
        data=request.body,
        headers={
            "content-type": "application/json",
            "x-forwarded-for": get_xff(request),
            "user-agent": get_user_agent(request),
        },
    )
    return HttpResponse(
        content=resp.content,
        status=resp.status_code,
        headers=EVENT_HEADERS,
    )

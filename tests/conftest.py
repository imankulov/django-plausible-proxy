from django.conf import settings


def pytest_configure():
    settings.configure(
        CACHES={
            "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
        },
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
            }
        ],
        INSTALLED_APPS=["plausible_proxy"],
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF="tests.urlconf",
    )

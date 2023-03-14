from django.conf import settings


def site_recaptcha_public_key(request):
    return {'site_recaptcha_public_key': settings.SITE_RECAPTCHA_PUBLIC_KEY}

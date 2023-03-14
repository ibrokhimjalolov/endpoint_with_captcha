import sys

import requests
from rest_framework.permissions import BasePermission

from django.conf import settings


class CaptchaRequired(BasePermission):
    """
    Check request for valid re-captcha
    define min_captcha_score in view
    """

    def has_permission(self, request, view):
        testing = sys.argv[1:2] == ["test"]
        if testing:
            # return True if testing
            return True
        captcha_token = request.headers.get("captcha-security")
        try:
            response = requests.post(
                f"https://www.google.com/recaptcha/api/siteverify?"
                f"secret={settings.SITE_RECAPTCHA_PRIVATE_KEY}&"
                f"response={captcha_token}"
            )
            data = response.json()
            """
            {
                "success": true,
                "challenge_ts": "2023-01-28T17:26:31Z",
                "hostname": "localhost",
                "score": 0.9,
                "action": "submit"
            }
            """
            if not data["success"]:
                return False
            # you can check for hostname also
            if data["score"] < getattr(view, "min_captcha_score", 0.7):
                return False
            return True
        except KeyError:
            return False

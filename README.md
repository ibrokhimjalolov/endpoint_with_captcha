## Endpoint'ni `recaptcha v3` bilan himoyalash

https://www.google.com/recaptcha/about/

### Asosiy ishlash logikasi
### Frontend `recaptcha`'dan `token` olib uni bizga malum bir `action` amalga oshirish uchun backend'ga http/https so'rovni header'ida `captcha-security: $token` korinishida yuboradi
### Backend header'dagi token'ni olib `recaptcha` apisidan tekshiradi va agar token valid bolsa `action`ni amalga oshiradi aks holda 403 qaytaradi.


## Backend tomondan implementatsiyasi
1. Bizga recaptcha service'sini ishlatishimiz uchun google console dan app ochishimiz kerak. project settings'da quyidagilarni kiritamiz
   ```
    SITE_RECAPTCHA_PRIVATE_KEY = "xxxxxxx"
    SITE_RECAPTCHA_PUBLIC_KEY = "yyyyyyyy"
   ```
2. `rest_framework` ishlatishimizni inobatga olib, eng optimal variant sifasida tekshiruvni `permission class` shaklida qilsak bo'ladi.
    ```
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

   ```
3. View'ni xafsizligini taminlash uchun `permission_classes` ga `CaptchaRequired` ni qo'shamiz (generic view ishlatgan holda albatta!)
    ```
    class MyView(APIView):
        permission_classes = [CaptchaRequired]
        def post(self, request):
            # ...
    ```
   
Plus'lari:
    Birgina `permission_classes = [CaptchaRequired]` qator orqali view xafsizligini taminlash.


# Asosiy qismi shular edi, endi backend developer endpoint'larni testlashi uchun swagger'ni moslash qoldi)

1. `endpoints/static/drf-yasg/swagger-ui-init.js` static fayl yaratish
2. `endpoints/templates/drf-yasg/swagger-ui.html` template yaratish
3. `endpoints/context_processors.py` context processor yaratish va template context_processors ga qo'shish
4. check swagger)

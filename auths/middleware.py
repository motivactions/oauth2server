from django.conf import settings
from django.apps import apps

REFERRAL_MODEL = getattr(settings, "REFERRAL_CODE_MODEL", "referrals.ReferralCode")
REFERRAL_PARAM_KEY = getattr(settings, "REFERRAL_PARAM_KEY", "ref_code")
REFERRAL_COOKIE_KEY = getattr(settings, "REFERRAL_COOKIE_KEY", "ref_code")
REFERRAL_COOKIE_AGE = getattr(settings, "REFERRAL_COOKIE_AGE", 60 * 60 * 24)


class ReferralLinkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ReferralCode = apps.get_model(REFERRAL_MODEL, require_ready=True)
        cookie_age = REFERRAL_COOKIE_AGE

        # Get user referrer from cookie referral code
        cookie_referral_code = request.COOKIES.get(REFERRAL_COOKIE_KEY, None)
        cookie_referrer = ReferralCode.get_user_from_code(cookie_referral_code)
        param_referrer = None
        request.referrer = cookie_referrer
        if cookie_referrer is None:
            # try get referral code from query parameter
            param_referral_code = request.GET.get(REFERRAL_PARAM_KEY, None)
            param_referrer = ReferralCode.get_user_from_code(param_referral_code)
            request.referrer = param_referrer
        response = self.get_response(request)
        if param_referrer is not None:
            response.set_cookie(
                REFERRAL_PARAM_KEY,
                str(param_referral_code),
                max_age=cookie_age,
            )
        return response

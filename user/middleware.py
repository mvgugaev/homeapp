from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class AuthRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_PAGE_URL)
        return None
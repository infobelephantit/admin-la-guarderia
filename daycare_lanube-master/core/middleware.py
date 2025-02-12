from django.shortcuts import reverse, redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from core.models.PageVisit import PageVisit
from django.contrib.auth.models import AnonymousUser
class ComingSoonModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")

        if settings.COMING_SOON_MODE and path!= reverse("coming-soon"):
            response = redirect(reverse("coming-soon"))
            return response

        response = self.get_response(request)

        return response

class CountVisitsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip admin or static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return
        if "HTTP_X_FORWARDED_FOR" in request.META:
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]
        ip_address = request.META.get('REMOTE_ADDR')
        if str(request.user) != 'AnonymousUser':
            page, created = PageVisit.objects.get_or_create(user=request.user)
            page.visit_count += 1
            page.ip_address = ip_address or None
            page.save()

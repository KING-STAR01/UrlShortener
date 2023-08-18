from django.http import JsonResponse
from django.urls import resolve
from rest_framework.authtoken.models import Token


class TokenRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.is_token_required(request):
            token_key = request.META.get("HTTP_AUTHORIZATION", "")
            try:
                token = Token.objects.get(key=token_key)
            except Token.DoesNotExist:
                return JsonResponse({"error": "Invalid Token"}, status=401)
        return response

    def is_token_required(self, request):
        required_urls = ["api/get_short_url/", "api/all_urls/"]
        resolved_url = resolve(request.path_info)
        return resolved_url.route in required_urls

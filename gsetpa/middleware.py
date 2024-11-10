from django.http import HttpResponse


class HealthCheckMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 400 and request.path == "/health":
            return HttpResponse()
        return response

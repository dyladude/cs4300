from django.conf import settings

class FixProxyRedirectMiddleware:
    """
    If a response Location header starts with /proxy/3000/proxy/3000/...,
    rewrite it to a single /proxy/3000/...  (or whatever FORCE_SCRIPT_NAME is).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.prefix = (getattr(settings, "FORCE_SCRIPT_NAME", "") or "")

    def __call__(self, request):
        response = self.get_response(request)
        if self.prefix and response.has_header("Location"):
            loc = response["Location"]
            double = self.prefix + self.prefix
            if loc.startswith(double):
                response["Location"] = loc[len(self.prefix):]
        return response

import logging

logger = logging.getLogger('api_method_logger')

class LogApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"API method called: {request.method}")
        response = self.get_response(request)

        return response
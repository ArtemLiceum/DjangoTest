import logging
from typing import Callable
from django.http import HttpResponse, HttpRequest

logger = logging.getLogger('api_method_logger')

class LogApiMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        logger.info(f"API method called: {request.method}")
        response = self.get_response(request)

        return response
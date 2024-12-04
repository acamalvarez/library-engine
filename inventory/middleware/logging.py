import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        request_data = {
            "ip_address": request.META.get("REMOTE_ADDR"),
            "method": request.method,
            "user": request.META.get("REMOTE_USER"),
            "hello": request.user,
        }

        logger.info(request_data)

        response = self.get_response(request)

        duration = time.time() - start_time
        response_dict = {
            "status_code": response.status_code,
            "duration": duration,
        }

        logger.info(response_dict)

        return response

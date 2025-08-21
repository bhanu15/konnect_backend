import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("app.middleware")
MAX_BODY_LOG = 2048

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id  # attach to request for logging

        try:
            body = (await request.body()).decode('utf-8') if request._receive else ''
        except Exception:
            body = '<unable to read request body>'

        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000

        # Read response body safely
        try:
            resp_body = b''
            async for chunk in response.body_iterator:
                resp_body += chunk
            new_response = Response(
                content=resp_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            resp_text = resp_body.decode('utf-8')[:MAX_BODY_LOG]
        except Exception:
            new_response = response
            resp_text = '<unable to read response body>'

        log = {
            'request_id': request_id,
            'method': request.method,
            'path': request.url.path,
            'status': response.status_code,
            'duration_ms': round(duration_ms, 2),
            'request_body': (body[:MAX_BODY_LOG] + '...') if len(body) > MAX_BODY_LOG else body,
            'response_body': resp_text
        }
        logger.info(log, extra={'request_id': request_id})

        # Add trace ID to response headers
        new_response.headers['X-Request-ID'] = request_id

        return new_response

"""
Transport and requests for HTTP protocol
"""
from typing import Optional, Dict

import httpx

from .base import BaseTransport, BaseRequest


HTTP_RETRY_MAX_COUNT = 5  # max retry count in case of http(s) errors
HTTP_RETRY_BACKOFF_FACTOR = 0.5  # backoff factor for Retry
HTTP_RETRY_STATUS_FORCELIST = {500, 502, 503, 504}  # status forcelist for Retry


class StandardHTTPTransport(BaseTransport):
    """ Standard HTTP Transport """

    def __init__(self, settings: Optional[Dict] = None):
        super().__init__(settings)
        self.settings.setdefault('max_retries', HTTP_RETRY_MAX_COUNT)
        self.settings.setdefault('handle_http_errors', True)

        default_headers = {'User-Agent': f'python-anycaptcha'}

        self.session_async = httpx.AsyncClient(
            headers=default_headers,
            timeout=httpx.Timeout(timeout=30)
        )

    async def _make_request_async(self, request_data: Dict) -> httpx.Response:
        if 'headers' not in request_data:
            request_data['headers'] = {}

        response = await self.session_async.request(**request_data)

        if self.settings['handle_http_errors']:
            response.raise_for_status()

        return response

    async def close_async(self):
        """ Close connections (async) """
        await self.session_async.aclose()


class HTTPRequestJSON(BaseRequest):
    """ HTTP Request that returns JSON response """

    def prepare(self, **kwargs) -> Dict:
        """ Prepares request """
        request = super().prepare(**kwargs)
        request.update(
            dict(headers={'Accept': 'application/json'})
        )
        return request

    def parse_response(self, response: httpx.Response) -> Dict:
        """ Parses response """
        return response.json()

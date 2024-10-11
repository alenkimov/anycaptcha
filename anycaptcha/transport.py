"""
Transport and requests for HTTP protocol
"""
import httpx


HTTP_RETRY_MAX_COUNT = 5  # max retry count in case of http(s) errors
HTTP_RETRY_BACKOFF_FACTOR = 0.5  # backoff factor for Retry
HTTP_RETRY_STATUS_FORCELIST = {500, 502, 503, 504}  # status forcelist for Retry


class HTTPRequestJSON:
    """ HTTP Request that returns JSON response """

    def __init__(self, service):
        # solving service instance
        self._service = service
        # source request data (not None if a request in process)
        self.source_data = None

    def process_response(self, response) -> dict:
        """ Parse response and clean source request data """
        response = self.parse_response(response)
        self.source_data = None
        return response

    def prepare(self, **kwargs) -> dict:
        """ Prepares request """
        self.source_data = kwargs
        request = {"headers": {'Accept': 'application/json'}}
        return request

    def parse_response(self, response: httpx.Response) -> dict:
        """ Parses response """
        return response.json()


class StandardHTTPTransport:
    """ Standard HTTP Transport """

    def __init__(self, settings: dict = None):
        self.settings = settings or {}
        self.settings.setdefault('max_retries', HTTP_RETRY_MAX_COUNT)
        self.settings.setdefault('handle_http_errors', True)

        default_headers = {'User-Agent': f'python-anycaptcha'}

        self.session = httpx.AsyncClient(
            headers=default_headers,
            timeout=httpx.Timeout(timeout=30)
        )

    async def make_request(self, request: HTTPRequestJSON, *args) -> dict:
        """ Makes a request to the service """
        request_data = request.prepare(*args)

        if 'headers' not in request_data:
            request_data['headers'] = {}

        response = await self.session.request(**request_data)

        if self.settings['handle_http_errors']:
            response.raise_for_status()

        return request.process_response(response)

    async def close(self):
        """ Close connections (async) """
        await self.session.aclose()

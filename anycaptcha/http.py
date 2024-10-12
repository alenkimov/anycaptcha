import httpx
from better_proxy import Proxy


# HTTP_RETRY_MAX_COUNT = 5  # max retry count in case of http(s) errors
# HTTP_RETRY_BACKOFF_FACTOR = 0.5  # backoff factor for Retry
# HTTP_RETRY_STATUS_FORCELIST = {500, 502, 503, 504}  # status forcelist for Retry


class AnycaptchaClient:
    def __init__(self, proxy: str | Proxy = None, **session_kwargs):
        session_kwargs['headers'] = session_kwargs.get('headers', {'user-agent': f'python-anycaptcha'})
        session_kwargs['timeout'] = session_kwargs.get('timeout', 5)
        proxy_url = Proxy.from_str(proxy).as_url if proxy else None
        self._session = httpx.AsyncClient(
            proxy=proxy_url,
            **session_kwargs,
        )

    async def close(self):
        """ Close connections (async) """
        await self._session.aclose()

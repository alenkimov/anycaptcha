from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class HCaptcha(BaseCaptcha):
    """ hCaptcha """

    site_key: str
    page_url: str
    is_invisible: bool = False
    api_domain: Optional[str] = None
    rqdata: Optional[str] = None


@dataclass
class HCaptchaSolution(BaseCaptchaSolution):
    """ hCaptcha solution """

    token: str

from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class FunCaptcha(BaseCaptcha):
    """ FunCaptcha """

    public_key: str
    page_url: str
    service_url: Optional[str] = None
    no_js: Optional[bool] = None
    blob: Optional[str] = None


@dataclass
class FunCaptchaSolution(BaseCaptchaSolution):
    """ FunCaptcha solution """

    token: str

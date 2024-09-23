from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class RecaptchaV2(BaseCaptcha):
    """ Google reCAPTCHA v2 """

    site_key: str
    page_url: str
    is_invisible: bool = False
    is_enterprise: bool = False
    data_s: Optional[str] = None
    api_domain: Optional[str] = None


@dataclass
class RecaptchaV2Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v2 solution """

    token: str

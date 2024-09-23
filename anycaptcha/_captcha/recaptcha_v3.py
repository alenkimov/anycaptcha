from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class RecaptchaV3(BaseCaptcha):
    """ Google reCAPTCHA v3 """

    site_key: str
    page_url: str
    is_enterprise: bool = False
    action: Optional[str] = None
    min_score: Optional[float] = None
    api_domain: Optional[str] = None


@dataclass
class RecaptchaV3Solution(BaseCaptchaSolution):
    """ Google reCAPTCHA v3 solution """

    token: str

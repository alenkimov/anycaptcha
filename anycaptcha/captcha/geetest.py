from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class GeeTest(BaseCaptcha):
    """ GeeTest """

    page_url: str
    gt_key: str
    challenge: str
    api_server: Optional[str] = None


@dataclass
class GeeTestSolution(BaseCaptchaSolution):
    """ GeeTest solution """

    challenge: str
    validate: str
    seccode: str

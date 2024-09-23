from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class CapyPuzzle(BaseCaptcha):
    """ Capy Puzzle CAPTCHA """

    site_key: str
    page_url: str
    api_server: Optional[str] = None


@dataclass
class CapyPuzzleSolution(BaseCaptchaSolution):
    """ Capy Puzzle CAPTCHA solution """

    captchakey: str
    challengekey: str
    answer: str

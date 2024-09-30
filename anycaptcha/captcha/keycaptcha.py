from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class KeyCaptcha(BaseCaptcha):
    """ KeyCaptcha """

    page_url: str
    user_id: str
    session_id: str
    ws_sign: str
    ws_sign2: str


@dataclass
class KeyCaptchaSolution(BaseCaptchaSolution):
    """ KeyCaptcha solution """

    token: str

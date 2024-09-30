from dataclasses import dataclass
from typing import Optional

from .base import BaseCaptcha, BaseCaptchaSolution
from ..enums import CaptchaAlphabet, WorkerLanguage


@dataclass
class TextCaptcha(BaseCaptcha):
    """ Text CAPTCHA """

    text: str
    alphabet: Optional[CaptchaAlphabet] = None
    language: Optional[WorkerLanguage] = None


@dataclass
class TextCaptchaSolution(BaseCaptchaSolution):
    """ Text CAPTCHA solution """

    text: str

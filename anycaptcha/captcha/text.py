from .base import BaseCaptcha, BaseCaptchaSolution
from ..enums import CaptchaAlphabet, WorkerLanguage


class TextCaptcha(BaseCaptcha):
    """ Text CAPTCHA """

    text: str
    alphabet: CaptchaAlphabet | None = None
    language: WorkerLanguage  | None = None


class TextCaptchaSolution(BaseCaptchaSolution):
    """ Text CAPTCHA solution """

    text: str

from dataclasses import dataclass

from .base import BaseCaptcha, BaseCaptchaSolution


@dataclass
class GeeTestV4(BaseCaptcha):
    """ GeeTest v4 """

    page_url: str
    captcha_id: str


@dataclass
class GeeTestV4Solution(BaseCaptchaSolution):
    """ GeeTest v4 solution """

    captcha_id: str
    lot_number: str
    pass_token: str
    gen_time: str
    captcha_output: str

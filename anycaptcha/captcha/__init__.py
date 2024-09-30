from .image import ImageCaptcha, ImageCaptchaSolution
from .text import TextCaptcha, TextCaptchaSolution
from .recaptcha_v2 import RecaptchaV2, RecaptchaV2Solution
from .recaptcha_v3 import RecaptchaV3, RecaptchaV3Solution
from .hcaptcha import HCaptcha, HCaptchaSolution
from .funcaptcha import FunCaptcha, FunCaptchaSolution
from .keycaptcha import KeyCaptcha, KeyCaptchaSolution
from .geetest import GeeTest, GeeTestSolution
from .geetest_v4 import GeeTestV4, GeeTestV4Solution
from .capy import CapyPuzzle, CapyPuzzleSolution
from .base import CaptchaType, BaseCaptchaSolution

__all__ = (
    'ImageCaptcha',
    'ImageCaptchaSolution',
    'TextCaptcha',
    'TextCaptchaSolution',
    'RecaptchaV2',
    'RecaptchaV2Solution',
    'RecaptchaV3',
    'RecaptchaV3Solution',
    'HCaptcha',
    'HCaptchaSolution',
    'FunCaptcha',
    'FunCaptchaSolution',
    'KeyCaptcha',
    'KeyCaptchaSolution',
    'GeeTest',
    'GeeTestSolution',
    'GeeTestV4',
    'GeeTestV4Solution',
    'CapyPuzzle',
    'CapyPuzzleSolution',
    'CaptchaType',
    'BaseCaptchaSolution',
)

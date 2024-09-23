"""
rucaptcha.com service
"""

# pylint: disable=unused-import
from .twocaptcha import (
    Service as Service2Captcha, GetBalanceRequest, GetStatusRequest,
    ReportGoodRequest, ReportBadRequest,
    ImageCaptchaTaskRequest, ImageCaptchaSolutionRequest,
    RecaptchaV2TaskRequest, RecaptchaV2SolutionRequest,
    RecaptchaV3TaskRequest, RecaptchaV3SolutionRequest,
    TextCaptchaTaskRequest, TextCaptchaSolutionRequest,
    FunCaptchaTaskRequest, FunCaptchaSolutionRequest,
    KeyCaptchaTaskRequest, KeyCaptchaSolutionRequest,
    GeeTestTaskRequest, GeeTestSolutionRequest,
    GeeTestV4TaskRequest, GeeTestV4SolutionRequest,
    HCaptchaTaskRequest, HCaptchaSolutionRequest,
    CapyPuzzleTaskRequest, CapyPuzzleSolutionRequest,
)

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest',
    'ImageCaptchaTaskRequest', 'ImageCaptchaSolutionRequest',
    'RecaptchaV2TaskRequest', 'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest', 'RecaptchaV3SolutionRequest',
    'TextCaptchaTaskRequest', 'TextCaptchaSolutionRequest',
    'FunCaptchaTaskRequest', 'FunCaptchaSolutionRequest',
    'KeyCaptchaTaskRequest', 'KeyCaptchaSolutionRequest',
    'GeeTestTaskRequest', 'GeeTestSolutionRequest',
    'GeeTestV4TaskRequest', 'GeeTestV4SolutionRequest',
    'HCaptchaTaskRequest', 'HCaptchaSolutionRequest',
    'CapyPuzzleTaskRequest', 'CapyPuzzleSolutionRequest',
]


class Service(Service2Captcha):
    """ Main service class for rucaptcha """

    BASE_URL = 'https://rucaptcha.com'

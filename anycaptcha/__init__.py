"""
All captcha solving services in one lib
"""

from .solver import Solver
from .service import Service
from .enums import CaptchaAlphabet
from .enums import CaptchaCharType
from .enums import WorkerLanguage
from .errors import AnyCaptchaException
from .errors import SolutionNotReadyYet
from .errors import ServiceError
from .errors import CaptchaError
from .errors import ProxyError
from .errors import AccessDeniedError
from .errors import LowBalanceError
from .errors import ServiceTooBusy
from .errors import SolutionWaitTimeout
from .errors import TooManyRequestsError
from .errors import MalformedRequestError
from .errors import BadInputDataError
from .errors import UnableToSolveError

from .captcha.image import ImageCaptcha, ImageCaptchaSolution
from .captcha.text import TextCaptcha, TextCaptchaSolution
from .captcha.recaptcha_v2 import RecaptchaV2, RecaptchaV2Solution
from .captcha.recaptcha_v3 import RecaptchaV3, RecaptchaV3Solution
from .captcha.hcaptcha import HCaptcha, HCaptchaSolution
from .captcha.funcaptcha import FunCaptcha, FunCaptchaSolution
from .captcha.keycaptcha import KeyCaptcha, KeyCaptchaSolution
from .captcha.geetest import GeeTest, GeeTestSolution
from .captcha.geetest_v4 import GeeTestV4, GeeTestV4Solution
from .captcha.capy import CapyPuzzle, CapyPuzzleSolution
from .captcha.base import CaptchaType, BaseCaptchaSolution

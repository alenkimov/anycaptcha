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

__all__ = [
    'Solver',
    'Service',
    'CaptchaAlphabet',
    'CaptchaCharType',
    'WorkerLanguage',
    'AnyCaptchaException',
    'SolutionNotReadyYet',
    'ServiceError',
    'CaptchaError',
    'ProxyError',
    'AccessDeniedError',
    'LowBalanceError',
    'ServiceTooBusy',
    'SolutionWaitTimeout',
    'TooManyRequestsError',
    'MalformedRequestError',
    'BadInputDataError',
    'UnableToSolveError',
]

class AnyCaptchaException(Exception):
    """Main exception class"""


class SolutionNotReadyYet(AnyCaptchaException):
    """CAPTCHA solving in progress"""


class ServiceError(AnyCaptchaException):
    """Main service-related exception class"""


class CaptchaError(AnyCaptchaException):
    """CAPTCHA-related exception"""


class ProxyError(AnyCaptchaException):
    """
    Bad proxy
    """


class AccessDeniedError(ServiceError):
    """
    Wrong API key
    IP banned
    IP not allowed
    """


class LowBalanceError(ServiceError):
    """
    Low balance
    """


class ServiceTooBusy(ServiceError):
    """
    No available slots
    """


class SolutionWaitTimeout(ServiceError):
    """
    Didn't receive solution within N minutes
    """


class TooManyRequestsError(ServiceError):
    """
    Exceeded request limit
    """


class MalformedRequestError(ServiceError):
    """
    Exceeded request limit
    """


class BadInputDataError(CaptchaError):
    """
    Not supported image file
    Empty file
    Image file is too big
    Bad captcha data (eg, wrong googlekey, bad page URL, etc.)
    """


class UnableToSolveError(CaptchaError):
    """
    Captcha unsolvable
    """

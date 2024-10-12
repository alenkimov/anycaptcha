import enum

from pydantic import BaseModel


class CaptchaType(enum.Enum):
    """ Captcha type enumeration """

    IMAGE = "ImageCaptcha"
    RECAPTCHAV2 = "RecaptchaV2"
    RECAPTCHAV3 = "RecaptchaV3"
    TEXT = "TextCaptcha"
    FUNCAPTCHA = "FunCaptcha"
    GEETEST = "GeeTest"
    GEETESTV4 = "GeeTestV4"
    HCAPTCHA = "HCaptcha"
    KEYCAPTCHA = "KeyCaptcha"
    CAPY = "CapyPuzzle"


class BaseCaptcha(BaseModel):
    """ Base class for any CAPTCHA """

    get_type: CaptchaType
    get_solution_class: 'BaseCaptchaSolution'

    def get_optional_data(self, **kwargs) -> Dict:
        """
        Return a dict with all optional fields requested (that are not None)
        as a dict with given names.

        :return: :dict:Dictionary of optional not None fields with given names and those values
        :rtype: dict
        """

        result = {}

        if not kwargs:
            # get all optional params
            kwargs = {
                field.name: (field.name, None) for field in fields(self)
                if field.default is not MISSING
            }

        for opt_field in kwargs:
            opt_field_value = getattr(self, opt_field)
            field_name, converter = kwargs[opt_field]
            if opt_field_value is not None:
                if callable(converter):
                    opt_field_value = converter(opt_field_value)
                result[field_name] = opt_field_value
        return result


class BaseCaptchaSolution(BaseModel):
    """ Base class for any CAPTCHA solution """
    get_type: CaptchaType
    get_captcha_class: BaseCaptcha

    def as_dict(self):
        """ Get solution data as Python dictionary """
        return self.model_dump()

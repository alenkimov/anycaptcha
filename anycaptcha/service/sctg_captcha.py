"""
azcaptcha.com service
"""
from better_proxy import Proxy

from .base import HTTPService
from ..transport import HTTPRequestJSON  # type: ignore
from .. import errors
from ..captcha import CaptchaType
from ..enums import CaptchaAlphabet

__all__ = [
    'Service', 'GetBalanceRequest', 'GetStatusRequest',
    'ReportGoodRequest', 'ReportBadRequest', 'RecaptchaV2TaskRequest'
]


class Service(HTTPService):
    """ Main service class for 2captcha """

    BASE_URL = 'http://api.sctg.xyz'

    def _post_init(self):
        """ Init settings """

        for captcha_type in self.settings:
            self.settings[captcha_type].polling_interval = 5
            self.settings[captcha_type].solution_timeout = 180
            if captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.HCAPTCHA):
                self.settings[captcha_type].polling_delay = 20
                self.settings[captcha_type].solution_timeout = 300
            elif captcha_type in (CaptchaType.RECAPTCHAV3,):
                self.settings[captcha_type].polling_delay = 15
            else:
                self.settings[captcha_type].polling_delay = 5


class Request(HTTPRequestJSON):
    """ Common Request class for 2captcha """

    def parse_response(self, response) -> dict:
        """ Parse response and checks for errors """

        response_data = super().parse_response(response)

        if response_data.pop("status") == 1:
            return response_data

        ###############
        # handle errors
        ###############
        error_code = response_data["request"]
        error_text = response_data.get("error_text", "")
        error_msg = f"{error_code}: {error_text}"

        if error_code == 'CAPCHA_NOT_READY':  # pylint: disable=no-else-raise
            raise errors.SolutionNotReadyYet()
        elif error_code in ('ERROR_WRONG_USER_KEY', 'ERROR_KEY_DOES_NOT_EXIST',
                            'ERROR_IP_NOT_ALLOWED', 'IP_BANNED'):
            raise errors.AccessDeniedError(error_msg)
        elif error_code in ('ERROR_ZERO_BALANCE',):
            raise errors.LowBalanceError(error_msg)
        elif error_code in ('ERROR_NO_SLOT_AVAILABLE',):
            # If server returns ERROR_NO_SLOT_AVAILABLE make a 5 seconds timeout before sending
            # next request.
            # time.sleep(5)
            raise errors.ServiceTooBusy(error_msg)
        elif error_code in ('MAX_USER_TURN',) or error_code.startswith('ERROR:'):
            raise errors.TooManyRequestsError(error_msg)
        elif error_code in ('ERROR_WRONG_ID_FORMAT', 'ERROR_WRONG_CAPTCHA_ID'):
            raise errors.MalformedRequestError(error_msg)
        elif error_code in ('ERROR_ZERO_CAPTCHA_FILESIZE', 'ERROR_TOO_BIG_CAPTCHA_FILESIZE',
                            'ERROR_WRONG_FILE_EXTENSION', 'ERROR_IMAGE_TYPE_NOT_SUPPORTED',
                            'ERROR_UPLOAD', 'ERROR_PAGEURL', 'ERROR_BAD_TOKEN_OR_PAGEURL',
                            'ERROR_GOOGLEKEY', 'ERROR_BAD_PARAMETERS', 'ERROR_TOKEN_EXPIRED',
                            'ERROR_EMPTY_ACTION'):
            raise errors.BadInputDataError(error_msg)
        elif error_code in ('ERROR_CAPTCHAIMAGE_BLOCKED', 'ERROR_CAPTCHA_UNSOLVABLE',
                            'ERROR_BAD_DUPLICATES'):
            raise errors.UnableToSolveError(error_msg)
        elif error_code in ('ERROR_BAD_PROXY', 'ERROR_PROXY_CONNECTION_FAILED'):
            raise errors.ProxyError(error_msg)

        raise errors.ServiceError(error_msg)


class InRequest(Request):
    """ Request class for requests to /in.php """

    def prepare(self, **kwargs) -> dict:
        """ Prepare request """

        request = super().prepare(**kwargs)
        request.update(
            dict(
                method="POST",
                url=self._service.BASE_URL + "/in.php",
                data=dict(
                    key=self._service.api_key,
                    json=1,
                    # soft_id=...
                )
            )
        )

        if 'headers' in request:
            del request['headers']

        return request


class ResRequest(Request):
    """ Request class for requests to /res.php """

    def prepare(self, **kwargs) -> dict:
        """ Prepare request """

        request = super().prepare(**kwargs)
        request.update(
            dict(
                method="GET",
                url=self._service.BASE_URL + "/res.php",
                params=dict(
                    key=self._service.api_key,
                    json=1
                )
            )
        )

        # azcaptcha.com doesn't like headers - returns ERROR_UPLOAD
        if 'headers' in request:
            del request['headers']

        return request


class GetBalanceRequest(ResRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare()
        request["params"].update(dict(action="getbalance"))
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return balance """

        return {'balance': float(super().parse_response(response)["request"])}


class GetStatusRequest(GetBalanceRequest):
    """ GetStatus Request class """

    def parse_response(self, response) -> dict:
        """ Parse response and return status """

        try:
            return super().parse_response(response)
        except errors.AnyCaptchaException:
            return {}


class ReportGoodRequest(ResRequest):
    """ ReportGood Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(solved_captcha=solved_captcha)
        request["params"].update(
            dict(
                action="reportgood",
                id=solved_captcha.captcha_id
            )
        )
        return request


class ReportBadRequest(ResRequest):
    """ ReportBad Request class """

    # pylint: disable=arguments-differ
    def prepare(self, solved_captcha) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(solved_captcha=solved_captcha)
        request["params"].update(
            dict(
                action="reportbad",
                id=solved_captcha.captcha_id
            )
        )
        return request


class TaskRequest(InRequest):
    """ Common Task Request class """

    # pylint: disable=arguments-differ,unused-argument
    def prepare(self, captcha, proxy: Proxy, user_agent, cookies):
        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        if proxy:
            request['data'].update(
                dict(
                    proxy=proxy.as_url,
                    proxytype=proxy.protocol.upper()
                )
            )

        if cookies:
            request['data']['cookies'] = ';'.join([f'{k}:{v}' for k, v in cookies.items()])

        if user_agent:
            request['data']['userAgent'] = user_agent

        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return task_id """

        response_data = super().parse_response(response)

        return dict(
            task_id=response_data.pop("request"),
            extra=response_data
        )


class SolutionRequest(ResRequest):
    """ Common Solution Request class """

    # pylint: disable=arguments-differ
    def prepare(self, task) -> dict:  # type: ignore
        """ Prepare a request """

        request = super().prepare(task=task)
        request["params"].update(
            dict(action="get", id=task.task_id)
        )
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)

        # get solution class
        solution_class = self.source_data['task'].captcha.get_solution_class()

        return dict(
            solution=solution_class(response_data.pop("request")),
            cost=None,
            extra=response_data
        )


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy: Proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="userrecaptcha",
                sitekey=captcha.site_key,
                pageurl=captcha.page_url,
                invisible=int(captcha.is_invisible)
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                data_s=('data-s', None)
            )
        )

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """

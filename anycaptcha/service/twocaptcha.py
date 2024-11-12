"""
2captcha.com service
"""

from better_proxy import Proxy

from .base import HTTPService
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import errors
from ..captcha import CaptchaType
from ..enums import CaptchaAlphabet

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


class Service(HTTPService):
    """ Main service class for 2captcha """

    BASE_URL = 'https://2captcha.com'
    CURRENCY: str = "RUB"

    def _post_init(self):
        """ Init settings """

        for captcha_type in self.settings:
            self.settings[captcha_type].polling_delay = 5
            self.settings[captcha_type].polling_interval = 5
            self.settings[captcha_type].solution_timeout = 180

            if captcha_type in (CaptchaType.RECAPTCHAV2, CaptchaType.HCAPTCHA):
                self.settings[captcha_type].polling_delay = 20
                self.settings[captcha_type].solution_timeout = 300
            elif captcha_type in (CaptchaType.RECAPTCHAV3,):
                self.settings[captcha_type].polling_delay = 15


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
                    soft_id=4704
                )
            )
        )
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
        return request


class GetBalanceRequest(ResRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:
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
        """ Prepare a request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        if proxy:
            proxy_without_protocol = (f"{proxy.login}:{proxy.password}@" if proxy.login and proxy.password else "") + f"{proxy.host}:{proxy.port}"
            request['data'].update(
                dict(
                    proxy=proxy_without_protocol,
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
        """ Prepare request """

        request = super().prepare(task=task)
        request["params"].update(
            dict(action="get2", id=task.task_id)
        )
        return request

    def parse_response(self, response) -> dict:
        """ Parse response and return solution and cost """

        response_data = super().parse_response(response)

        solution_data = response_data.pop("request")
        solution_class = self.source_data['task'].captcha.get_solution_class()
        captcha_type = self.source_data['task'].captcha.get_type()
        if captcha_type == CaptchaType.GEETEST:
            solution = solution_class(
                challenge=solution_data['geetest_challenge'],
                validate=solution_data['geetest_validate'],
                seccode=solution_data['geetest_seccode']
            )
        elif captcha_type == CaptchaType.GEETESTV4:
            solution = solution_class(
                captcha_id=solution_data['captcha_id'],
                lot_number=solution_data['lot_number'],
                pass_token=solution_data['pass_token'],
                gen_time=solution_data['gen_time'],
                captcha_output=solution_data['captcha_output'],
            )
        elif captcha_type == CaptchaType.CAPY:
            solution = solution_class(**solution_data)
        else:
            solution = solution_class(solution_data)

        price = None
        if 'price' in response_data:
            price = response_data.pop("price")

        return dict(
            solution=solution,
            cost=price,
            extra=response_data
        )


class ImageCaptchaTaskRequest(TaskRequest):
    """ ImageCaptchaTask Request class """

    # pylint: disable=arguments-differ,unused-argument,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        # add required params
        request['data'].update(
            dict(
                method="base64",
                body=captcha.get_image_base64().decode('ascii')
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                is_phrase=('phrase', lambda v: int(bool(v))),
                is_case_sensitive=('regsense', lambda v: int(bool(v))),
                char_type=('numeric', lambda v: v.value),
                is_math=('calc', lambda v: int(bool(v))),
                min_len=('min_len', None),
                max_len=('max_len', None),
                alphabet=('language',
                          lambda v: {CaptchaAlphabet.CYRILLIC: 1,
                                     CaptchaAlphabet.LATIN: 2}.get(v, 0)),
                language=('lang', lambda v: v.value),
                comment=('textinstructions', None),
            )
        )

        return request


class ImageCaptchaSolutionRequest(SolutionRequest):
    """ Image CAPTCHA solution request """


class RecaptchaV2TaskRequest(TaskRequest):
    """ reCAPTCHA v2 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
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
                googlekey=captcha.site_key,
                pageurl=captcha.page_url,
                invisible=int(captcha.is_invisible)
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                data_s=('data-s', None),
                api_domain=('domain', None)
            )
        )

        # check if enterprise captcha
        if captcha.is_enterprise:
            request['data']['enterprise'] = 1

        return request


class RecaptchaV2SolutionRequest(SolutionRequest):
    """ reCAPTCHA v2 solution request """


class RecaptchaV3TaskRequest(TaskRequest):
    """ reCAPTCHA v3 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
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
                version="v3",
                googlekey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                action=('action', None),
                min_score=('min_score', None),
                api_domain=('domain', None)
            )
        )

        # check if enterprise captcha
        if captcha.is_enterprise:
            request['data']['enterprise'] = 1

        return request


class RecaptchaV3SolutionRequest(SolutionRequest):
    """ reCAPTCHA v3 solution request """


class TextCaptchaTaskRequest(TaskRequest):
    """ TextCaptcha task request """

    # pylint: disable=arguments-differ,unused-argument,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                textcaptcha=captcha.text
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                alphabet=('language',
                          lambda v: {CaptchaAlphabet.CYRILLIC: 1,
                                     CaptchaAlphabet.LATIN: 2}.get(v, 0)),
                language=('lang', lambda v: v.value)
            )
        )

        return request


class TextCaptchaSolutionRequest(SolutionRequest):
    """ TextCaptcha solution request """


class FunCaptchaTaskRequest(TaskRequest):
    """ FunCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="funcaptcha",
                publickey=captcha.public_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                service_url=('surl', None),
                no_js=('nojs', None),
                blob=('data[blob]', None),
            )
        )

        return request


class FunCaptchaSolutionRequest(SolutionRequest):
    """ FunCaptcha solution request """


class KeyCaptchaTaskRequest(TaskRequest):
    """ KeyCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="keycaptcha",
                s_s_c_user_id=captcha.user_id,
                s_s_c_session_id=captcha.session_id,
                s_s_c_web_server_sign=captcha.ws_sign,
                s_s_c_web_server_sign2=captcha.ws_sign2,
                pageurl=captcha.page_url
            )
        )

        return request


class KeyCaptchaSolutionRequest(SolutionRequest):
    """ KeyCaptcha solution request """


class GeeTestTaskRequest(TaskRequest):
    """ GeeTest task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="geetest",
                gt=captcha.gt_key,
                challenge=captcha.challenge,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                api_server=('api_server', None)
            )
        )

        return request


class GeeTestSolutionRequest(SolutionRequest):
    """ GeeTest solution request """


class HCaptchaTaskRequest(TaskRequest):
    """ HCaptcha task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="hcaptcha",
                sitekey=captcha.site_key,
                pageurl=captcha.page_url,
                invisible=int(captcha.is_invisible),
            )
        )

        request['data'].update(
            captcha.get_optional_data(
                data=('rqdata', None)
            )
        )

        request['data'].update(
            captcha.get_optional_data(
                api_domain=('domain', None)
            )
        )

        return request


class HCaptchaSolutionRequest(SolutionRequest):
    """ HCaptcha solution request """


class CapyPuzzleTaskRequest(TaskRequest):
    """ CapyPuzzle task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="capy",
                captchakey=captcha.site_key,
                pageurl=captcha.page_url
            )
        )

        # add optional params
        request['data'].update(
            captcha.get_optional_data(
                api_server=('api_server', None)
            )
        )

        return request


class CapyPuzzleSolutionRequest(SolutionRequest):
    """ CapyPuzzle solution request """


class GeeTestV4TaskRequest(TaskRequest):
    """ GeeTest v4 task request """

    # pylint: disable=arguments-differ,signature-differs
    def prepare(self, captcha, proxy, user_agent, cookies) -> dict:  # type: ignore
        """ Prepare request """

        request = super().prepare(
            captcha=captcha,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )

        request['data'].update(
            dict(
                method="geetest_v4 ",
                captcha_id=captcha.captcha_id,
                pageurl=captcha.page_url
            )
        )

        return request


class GeeTestV4SolutionRequest(SolutionRequest):
    """ GeeTest v4 solution request """

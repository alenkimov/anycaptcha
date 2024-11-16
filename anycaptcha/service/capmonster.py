from typing import Any, Dict

from better_proxy import Proxy

from .base import HTTPService, CaptchaTask
from .._transport.http_transport import HTTPRequestJSON  # type: ignore
from .. import errors
from ..captcha import CaptchaType
from ..enums import CaptchaAlphabet

__all__ = [
    'Service', 'CreateTaskRequest', 'GetTaskResultRequest',
    'GetBalanceRequest',
    'RecaptchaV2TaskRequest',
    'RecaptchaV2SolutionRequest',
    'RecaptchaV3TaskRequest',
    'RecaptchaV3SolutionRequest'
]


class Service(HTTPService):
    """ Main service class for CapMonster """

    BASE_URL = 'https://api.capmonster.cloud'

    def _post_init(self):
        """ Initialize settings """
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


class CapMonsterRequest(HTTPRequestJSON):
    """ Common Request class for CapMonster """

    def parse_response(self, response) -> dict:
        """ Parse response and check for errors """
        response_data = super().parse_response(response)

        if response_data.get("errorId") == 0:
            return response_data
        else:
            error_code = response_data.get("errorCode", "UNKNOWN_ERROR")
            error_msg = f"{response_data.get('errorDescription', '')} ({error_code})"

            # Map CapMonster error codes to library errors
            if error_code == 'ERROR_CAPTCHA_UNSOLVABLE':
                raise errors.UnableToSolveError(error_msg)
            elif error_code in ('ERROR_WRONG_CLIENT_KEY', 'ERROR_KEY_DOES_NOT_EXIST',
                                'ERROR_IP_NOT_ALLOWED', 'IP_BANNED'):
                raise errors.AccessDeniedError(error_msg)
            elif error_code == 'ERROR_ZERO_BALANCE':
                raise errors.LowBalanceError(error_msg)
            elif error_code == 'ERROR_TOO_MANY_TASKS':
                raise errors.TooManyRequestsError(error_msg)
            elif error_code == 'ERROR_PROXY':
                raise errors.ProxyError(error_msg)
            else:
                raise errors.ServiceError(error_msg)


class CreateTaskRequest(CapMonsterRequest):
    """ CreateTask Request class """

    def prepare(self, task_data: dict) -> dict:
        """ Prepare request to create a task """
        request_payload = {
            "clientKey": self._service.api_key,
            "task": task_data
        }

        return {
            "method": "POST",
            "url": f"{self._service.BASE_URL}/createTask",
            "json": request_payload
        }

    def parse_response(self, response) -> dict:
        """ Parse response and return task_id """
        response_data = super().parse_response(response)
        return {
            "task_id": response_data.get("taskId")
        }


class GetBalanceRequest(CapMonsterRequest):
    """ GetBalance Request class """

    def prepare(self) -> dict:
        """ Prepare request to get balance """
        request_payload = {
            "clientKey": self._service.api_key
        }
        return {
            "method": "POST",
            "url": f"{self._service.BASE_URL}/getBalance",
            "json": request_payload
        }

    def parse_response(self, response) -> dict:
        """ Parse response and return balance """
        response_data = super().parse_response(response)
        return {
            "balance": float(response_data.get("balance", 0.0))
        }


class HCaptchaTaskRequest(CreateTaskRequest):
    """ hCaptcha task request for CapMonster """

    def prepare(self, captcha, proxy: Proxy = None, user_agent: str = None, cookies: dict = None) -> dict:
        """ Prepare createTask request for hCaptcha """
        task = {
            "type": "HCaptchaTaskProxyless" if proxy is None else "HCaptchaTask",
            "websiteURL": captcha.page_url,
            "websiteKey": captcha.site_key,
        }

        if proxy:
            task.update({
                "proxy": proxy.as_url.split("://")[1]
            })

        if user_agent:
            task["userAgent"] = user_agent

        if captcha.is_invisible:
            task["isInvisible"] = True

        if captcha.rqdata:
            task["data"] = captcha.rqdata

        if cookies:
            task["cookies"] = '; '.join(f'{k}={v}' for k, v in cookies.items())

        return super().prepare(task_data=task)


class RecaptchaV2TaskRequest(CreateTaskRequest):
    """ reCAPTCHA v2 task request for CapMonster """

    def prepare(self, captcha, proxy: Proxy = None, user_agent: str = None, cookies: dict = None) -> dict:
        """ Prepare createTask request for ReCaptcha V2 """
        task = {
            "type": "RecaptchaV2TaskProxyless" if proxy is None else "RecaptchaV2Task",
            "websiteURL": captcha.page_url,
            "websiteKey": captcha.site_key,
            "isInvisible": int(captcha.is_invisible) if hasattr(captcha, 'is_invisible') else 0
        }

        if proxy:
            task.update({
                "proxy": proxy.as_url.split("://")[1]
            })

        if user_agent:
            task["userAgent"] = user_agent

        # Handle optional recaptchaDataSValue if present
        if hasattr(captcha, 'recaptcha_data_s_value') and captcha.recaptcha_data_s_value:
            task["recaptchaDataSValue"] = captcha.recaptcha_data_s_value

        return super().prepare(task_data=task)


class RecaptchaV3TaskRequest(CreateTaskRequest):
    """ reCAPTCHA v3 task request for CapMonster """

    def prepare(self, captcha, proxy: Proxy = None, user_agent: str = None, cookies: dict = None) -> dict:
        """ Prepare createTask request for ReCaptcha V3 """
        task = {
            "type": "RecaptchaV3TaskProxyless",
            "websiteURL": captcha.page_url,
            "websiteKey": captcha.site_key,
        }

        # Handle optional minScore and pageAction
        if hasattr(captcha, 'min_score') and captcha.min_score is not None:
            task["minScore"] = captcha.min_score

        if hasattr(captcha, 'page_action') and captcha.page_action:
            task["pageAction"] = captcha.page_action

        return super().prepare(task_data=task)


class GetTaskResultRequest(CapMonsterRequest):
    """ GetTaskResult Request class for CapMonster """

    def prepare(self, task: 'CaptchaTask') -> dict:
        request = super().prepare(task=task)

        request.update({
            "url": f"{self._service.BASE_URL}/getTaskResult",
            "method": "POST",
            "json": {
                "clientKey": self._service.api_key,
                "taskId": str(task.task_id)
            }
        })

        return request

    def parse_response(self, response) -> dict:
        response_data = super().parse_response(response)

        return dict(
            solution=response_data.get("solution"),
            cost=response_data.get("cost"),
            extra=response_data,
            status=response_data.get("status")
        )


class HCaptchaSolutionRequest(GetTaskResultRequest):
    """ HCaptcha solution request for CapMonster """

    def parse_response(self, response) -> Dict[str, Any]:
        response_data = super().parse_response(response)

        if response_data["status"] != "ready":
            raise errors.SolutionNotReadyYet()

        solution_class = self.source_data['task'].captcha.get_solution_class()
        solution = solution_class(response_data.get("solution").get("gRecaptchaResponse"))

        if not solution:
            raise errors.ServiceError("Missing gRecaptchaResponse in solution.")

        return dict(
            solution=solution,
        )


class RecaptchaV2SolutionRequest(GetTaskResultRequest):
    """ reCAPTCHA v2 solution request for CapMonster """

    def parse_response(self, response) -> Dict[str, Any]:
        response_data = super().parse_response(response)

        if response_data["status"] != "ready":
            raise errors.SolutionNotReadyYet()

        solution_class = self.source_data['task'].captcha.get_solution_class()
        solution = solution_class(response_data.get("solution").get("gRecaptchaResponse"))

        if not solution:
            raise errors.ServiceError("Missing gRecaptchaResponse in solution.")

        return dict(
            solution=solution,
        )


class RecaptchaV3SolutionRequest(GetTaskResultRequest):
    """ reCAPTCHA v3 solution request for CapMonster """

    def parse_response(self, response) -> Dict[str, Any]:
        response_data = super().parse_response(response)

        if response_data["status"] != "ready":
            raise errors.SolutionNotReadyYet()

        solution_class = self.source_data['task'].captcha.get_solution_class()
        solution = solution_class(response_data.get("solution").get("gRecaptchaResponse"))

        if not solution:
            raise errors.ServiceError("Missing gRecaptchaResponse in solution.")

        return dict(
            solution=solution,
        )

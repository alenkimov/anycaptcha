import enum
from . import (
    anti_captcha,
    azcaptcha,
    captcha_guru,
    cptch_net,
    deathbycaptcha,
    rucaptcha,
    twocaptcha,
)


class Service(enum.Enum):
    """CAPTCHA solving service enum"""

    ANTI_CAPTCHA   = "anti-captcha.com"
    AZCAPTCHA      = "azcaptcha.com"
    CAPTCHA_GURU   = "cap.guru"
    CPTCH_NET      = "cptch.net"
    DEATHBYCAPTCHA = "deathbycaptcha.com"
    RUCAPTCHA      = "rucaptcha.com"
    TWOCAPTCHA     = "2captcha.com"


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    Service.ANTI_CAPTCHA: anti_captcha,
    Service.AZCAPTCHA: azcaptcha,
    Service.CAPTCHA_GURU: captcha_guru,
    Service.CPTCH_NET: cptch_net,
    Service.DEATHBYCAPTCHA: deathbycaptcha,
    Service.RUCAPTCHA: rucaptcha,
    Service.TWOCAPTCHA: twocaptcha
}
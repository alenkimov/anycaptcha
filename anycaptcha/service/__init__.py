from ..enums import Service

from . import (
    anti_captcha,
    azcaptcha,
    captcha_guru,
    cptch_net,
    deathbycaptcha,
    rucaptcha,
    twocaptcha,
    multibot_captcha,
    sctg_captcha,
    capmonster,
    capsolver
)


# supported CAPTCHA solving services
SOLVING_SERVICE = {
    Service.ANTI_CAPTCHA: anti_captcha,
    Service.AZCAPTCHA: azcaptcha,
    Service.CAPTCHA_GURU: captcha_guru,
    Service.CPTCH_NET: cptch_net,
    Service.DEATHBYCAPTCHA: deathbycaptcha,
    Service.RUCAPTCHA: rucaptcha,
    Service.TWOCAPTCHA: twocaptcha,
    Service.MULTIBOT_CAPTCHA: multibot_captcha,
    Service.SCTG_CAPTCHA: sctg_captcha,
    Service.CAPMONSTER: capmonster,
    Service.CAPSOLVER: capsolver
}

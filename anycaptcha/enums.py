from enum import StrEnum, IntEnum


class Service(StrEnum):
    """CAPTCHA solving service enum"""

    ANTI_CAPTCHA        = "anti-captcha.com"
    AZCAPTCHA           = "azcaptcha.com"
    CAPTCHA_GURU        = "cap.guru"
    CPTCH_NET           = "cptch.net"
    DEATHBYCAPTCHA      = "deathbycaptcha.com"
    RUCAPTCHA           = "rucaptcha.com"
    TWOCAPTCHA          = "2captcha.com"
    MULTIBOT_CAPTCHA    = "multibot.in"
    SCTG_CAPTCHA        = "api.sctg.xyz"
    CAPMONSTER          = "capmonster.cloud"
    CAPSOLVER           = "capsolver.com"

    def __str__(self):
        return self.value


class CaptchaType(StrEnum):
    """ Captcha type enumeration """

    IMAGE       = "ImageCaptcha"
    RECAPTCHAV2 = "RecaptchaV2"
    RECAPTCHAV3 = "RecaptchaV3"
    TEXT        = "TextCaptcha"
    FUNCAPTCHA  = "FunCaptcha"
    GEETEST     = "GeeTest"
    GEETESTV4   = "GeeTestV4"
    HCAPTCHA    = "HCaptcha"
    KEYCAPTCHA  = "KeyCaptcha"
    CAPY        = "CapyPuzzle"


class CaptchaAlphabet(StrEnum):
    """ Alphabet used in the CAPTCHA """

    LATIN = 'latin'
    CYRILLIC = 'cyrillic'


class CaptchaCharType(IntEnum):
    """ Character types used in CAPTCHA """

    NUMERIC = 1
    ALPHA = 2
    ALPHA_OR_NUMERIC = 3
    ALPHANUMERIC = 4


class WorkerLanguage(StrEnum):
    """ Worker's language to solve the CAPTCHA """

    ENGLISH = 'en'
    RUSSIAN = 'ru'
    SPANISH = 'es'
    PORTUGUESE = 'pt'
    UKRAINIAN = 'uk'
    VIETNAMESE = 'vi'
    FRENCH = 'fr'
    INDONESIAN = 'id'
    ARAB = 'ar'
    JAPANESE = 'ja'
    TURKISH = 'tr'
    GERMAN = 'de'
    CHINESE = 'zh'
    POLISH = 'pl'
    THAI = 'th'
    ITALIAN = 'it'
    DUTCH = 'nl'
    SLOVAK = 'sk'
    BULGARIAN = 'bg'
    ROMANIAN = 'ro'
    HUNGARIAN = 'hu'
    KOREAN = 'ko'
    CZECH = 'cs'
    AZERBAIJANI = 'az'
    PERSIAN = 'fa'
    BENGALI = 'bn'
    GREEK = 'el'
    LITHUANIAN = 'lt'
    LATVIAN = 'lv'
    SWEDISH = 'sv'
    SERBIAN = 'sr'
    CROATIAN = 'hr'
    HEBREW = 'he'
    HINDI = 'hi'
    NORWEGIAN = 'nb'
    SLOVENIAN = 'sl'
    DANISH = 'da'
    UZBEK = 'uz'
    FINNISH = 'fi'
    CATALAN = 'ca'
    GEORGIAN = 'ka'
    MALAY = 'ms'
    TELUGU = 'te'
    ESTONIAN = 'et'
    MALAYALAM = 'ml'
    BELORUSSIAN = 'be'
    KAZAKH = 'kk'
    MARATHI = 'mr'
    NEPALI = 'ne'
    BURMESE = 'my'
    BOSNIAN = 'bs'
    ARMENIAN = 'hy'
    MACEDONIAN = 'mk'
    PUNJABI = 'pa'

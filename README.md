# anycaptcha

[![Telegram channel](https://img.shields.io/endpoint?color=neon&url=https://tg.sumanjay.workers.dev/cum_insider)](https://t.me/cum_insider)
[![PyPI version info](https://img.shields.io/pypi/v/anycaptcha.svg)](https://pypi.python.org/pypi/anycaptcha)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/anycaptcha.svg)](https://pypi.python.org/pypi/anycaptcha)
[![PyPI downloads per month](https://img.shields.io/pypi/dm/anycaptcha.svg)](https://pypi.python.org/pypi/anycaptcha)

```bash
pip install anycaptcha
```

anycaptcha is a unified Python API for CAPTCHA solving services.

Special thanks to [unicaps](https://github.com/sergey-scat/unicaps) lib

## Key Features
- A unified Python interface that is independent of the service used
- Uses native service protocol/endpoints (eg, no needs in patching _hosts_ file)
- Modern asynchronous client
- Supports 10 types of CAPTCHAs
- Written Pythonic way and is intended for humans
- Supports proxies in any format thanks to [better-proxy](https://github.com/alenkimov/better_proxy)

Supports 9 CAPTCHA solving services:
- [2captcha.com](http://2captcha.com/?from=12016127)	                     
- [rucaptcha.com](https://rucaptcha.com?from=12016127)                       
- [anti-captcha.com](https://getcaptchasolution.com/tmb2cervod)              
- [azcaptcha.com](https://azcaptcha.com)                                     
- [cap.guru](https://cap.guru/ru)                                            
- [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b)
- [capsolver.com](https://dashboard.capsolver.com/passport/register?inviteCode=m-aE3NeBGZLU)
- [capmonster.cloud](https://capmonster.cloud)
- [multibot.in](https://multibot.in)

## Example
```python
from pathlib import Path
from anycaptcha import Solver, Service

API_KEY = '<PLACE_YOUR_API_KEY_HERE>'


async def main():
    async with Solver(Service.TWOCAPTCHA, API_KEY) as solver:
        solved = await solver.solve_image_captcha(
            Path("captcha.jpg"),
            is_phrase=False,
            is_case_sensitive=True
        )
        print(f'CAPTCHA text: {solved.solution.text}')
        await solved.report_good()
```

## Supported CAPTCHAs / Services

| Service                                                                     | Image | Text | [reCAPTCHA v2](https://developers.google.com/recaptcha/docs/display) | [reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) | [FunCaptcha](https://funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC) | [KeyCAPTCHA](https://www.keycaptcha.com/) | [Geetest](https://www.geetest.com/en/demo) | [Geetest v4](https://www.geetest.com/en/demo) | [hCaptcha](https://www.hcaptcha.com/) | [Capy](https://www.capy.me/) |
|-----------------------------------------------------------------------------|:-----:|:----:|:--------------------------------------------------------------------:|:---------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-----------------------------------------:|:------------------------------------------:|:---------------------------------------------:|:-------------------------------------:|:----------------------------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |   ✅   |  ✅   |                                  ✅                                   |                                ✅                                |                                              ✅                                              |                     ✅                     |                     ✅                      |                       ✅                       |                   ✅                   |              ✅               |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |   ✅   |  ✅   |                                  ✅                                   |                                ✅                                |                                              ✅                                              |                     ✅                     |                     ✅                      |                       ✅                       |                   ✅                   |              ✅               |
| [anti-captcha.com](https://getcaptchasolution.com/tmb2cervod)               |   ✅   |  ❌   |                                  ✅                                   |                                ✅                                |                                              ✅                                              |                     ❌                     |                     ✅                      |                       ✅                       |                   ✅                   |              ❌               |
| [azcaptcha.com](https://azcaptcha.com)                                      |   ✅   |  ❌   |                                  ✅                                   |                                ✅                                |                                              ✅                                              |                     ❌                     |                     ❌                      |                       ❌                       |                   ✅                   |              ❌               |
| [cap.guru](https://cap.guru/ru)                                             |   ✅   |  ❌   |                                  ✅                                   |                                ✅                                |                                              ❌                                              |                     ❌                     |                     ✅                      |                       ❌                       |                   ✅                   |              ❌               |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |   ✅   |  ❌   |                                  ✅                                   |                                ✅                                |                                              ✅                                              |                     ❌                     |                     ❌                      |                       ❌                       |                   ✅                   |              ❌               |

### Image CAPTCHA

| Service                                                                     | Regular | Case Sensitive | Phrase | Numbers only | Letters only | Math | Length |    Language    | Comment for worker |
|-----------------------------------------------------------------------------|:-------:|:--------------:|:------:|:------------:|:------------:|:----:|:------:|:--------------:|:------------------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |       ✅        |   ✅    |      ✅       |      ✅       |  ✅   |   ✅    | Cyrillic/Latin |         ✅          |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |       ✅        |   ✅    |      ✅       |      ✅       |  ✅   |   ✅    | Cyrillic/Latin |         ✅          |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |       ✅        |   ✅    |      ✅       |      ✅       |  ✅   |   ✅    |     Latin      |         ✅          |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ✅    |       ❌        |   ❌    |      ❌       |      ❌       |  ❌   |   ❌    |     Latin      |         ✅          |
| [cap.guru](https://cap.guru/ru)                                             |    ✅    |       ❌        |   ❌    |      ❌       |      ❌       |  ❌   |   ❌    |     Latin      |         ✅          |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ✅    |       ❌        |   ❌    |      ❌       |      ❌       |  ❌   |   ❌    |     Latin      |         ❌          |

### Text CAPTCHA

Text Captcha is a type of captcha that is represented as text and doesn't contain images.
Usually you have to answer a question to pass the verification.
For example: "If tomorrow is Saturday, what day is today?".

| Service                                                                     |     Language     |
|-----------------------------------------------------------------------------|:----------------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         | English, Russian |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        | English, Russian |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |        ❌         |
| [azcaptcha.com](https://azcaptcha.com)                                      |        ❌         |
| [cap.guru](https://cap.guru/ru)                                             |        ❌         |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |        ❌         |

### reCAPTCHA v2

| Service                                                                     | Regular | Invisible | Enterprise | Google service<sup>1</sup> | Proxy<sup>2</sup> | Cookies<sup>3</sup> | User-Agent<sup>4</sup> |
|-----------------------------------------------------------------------------|:-------:|:---------:|:----------:|:--------------------------:|:-----------------:|:-------------------:|:----------------------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |     ✅     |     ✅      |             ✅              |         ✅         |          ✅          |           ✅            |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |     ✅     |     ✅      |             ✅              |         ✅         |          ✅          |           ✅            |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |     ✅     |     ✅      |             ✅              |         ✅         |          ✅          |           ✅            |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ✅    |     ✅     |     ❌      |             ✅              |         ✅         |          ✅          |           ✅            |
| [cap.guru](https://cap.guru/ru)                                             |    ✅    |     ✅     |     ❌      |             ✅              |         ✅         |          ✅          |           ✅            |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ✅    |     ✅     |     ❌      |             ✅              |         ✅         |          ❌          |           ❌            |

<sup>1</sup> Support of solving reCAPTCHA on Google services (e.g. Google Search) </br>
<sup>2</sup> Support of solving via proxy server </br>
<sup>3</sup> Support of passing custom cookies </br>
<sup>4</sup> Support of passing custom User-Agent header </br>

### reCAPTCHA v3

| Service                                                                     | Regular | Enterprise | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:----------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |     ✅      |   ❌   |    ❌    |     ❌      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |     ✅      |   ❌   |    ❌    |     ❌      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |     ✅      |   ❌   |    ❌    |     ❌      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ✅    |     ❌      |   ✅   |    ❌    |     ❌      |
| [cap.guru](https://cap.guru/ru)                                             |    ✅    |     ❌      |   ✅   |    ✅    |     ✅      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ✅    |     ❌      |   ✅   |    ❌    |     ❌      |

### FunCaptcha (Arkose Labs)

| Service                                                                     | Regular | Data (BLOB) | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:-----------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |      ✅      |   ✅   |    ❌    |     ✅      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |      ✅      |   ✅   |    ❌    |     ✅      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |      ✅      |   ✅   |    ❌    |     ✅      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ✅    |      ✅      |   ✅   |    ❌    |     ✅      |
| [cap.guru](https://cap.guru/ru)                                             |    ❌    |      ❌      |   ❌   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ✅    |      ❌      |   ✅   |    ❌    |     ❌      |

### KeyCAPTCHA

| Service                                                                     | Regular | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |   ❌   |    ❌    |     ❌      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |   ❌   |    ❌    |     ❌      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ❌    |   ❌   |    ❌    |     ❌      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ❌    |   ❌   |    ❌    |     ❌      |
| [cap.guru](https://cap.guru/ru)                                             |    ❌    |   ❌   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ❌    |   ❌   |    ❌    |     ❌      |

### Geetest

| Service                                                                     | Regular | API server | GetLib | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:----------:|:------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |     ✅      |   ❌    |   ✅   |    ❌    |     ✅      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |     ✅      |   ❌    |   ✅   |    ❌    |     ✅      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |     ✅      |   ✅    |   ✅   |    ❌    |     ✅      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ❌    |     ❌      |   ❌    |   ❌   |    ❌    |     ❌      |
| [cap.guru](https://captcha.guru/ru)                                         |    ✅    |     ❌      |   ❌    |   ✅   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ❌    |     ❌      |   ❌    |   ❌   |    ❌    |     ❌      |

### Geetest v4

| Service                                                                     | Regular | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |   ✅   |    ❌    |     ✅      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |   ✅   |    ❌    |     ✅      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |   ✅   |    ❌    |     ✅      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ❌    |   ❌   |    ❌    |     ❌      |
| [cap.guru](https://cap.guru/ru)                                             |    ❌    |   ❌   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ❌    |   ❌   |    ❌    |     ❌      |

### hCaptcha

| Service                                                                     | Regular | Invisible | Custom Data | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:---------:|:-----------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |     ✅     |      ✅      |   ✅   |    ❌    |     ✅      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |     ✅     |      ✅      |   ✅   |    ❌    |     ✅      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ✅    |     ✅     |      ❌      |   ✅   |    ❌    |     ✅      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ✅    |     ❌     |      ❌      |   ✅   |    ❌    |     ❌      |
| [cap.guru](https://cap.guru/ru)                                             |    ✅    |     ❌     |      ❌      |   ✅   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ✅    |     ❌     |      ❌      |   ✅   |    ❌    |     ❌      |

### Capy Puzzle

| Service                                                                     | Regular | API server | Proxy | Cookies | User-Agent |
|-----------------------------------------------------------------------------|:-------:|:----------:|:-----:|:-------:|:----------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |    ✅    |     ✅      |   ✅   |    ❌    |     ❌      |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |    ✅    |     ✅      |   ✅   |    ❌    |     ❌      |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |    ❌    |     ❌      |   ❌   |    ❌    |     ❌      |
| [azcaptcha.com](https://azcaptcha.com)                                      |    ❌    |     ❌      |   ❌   |    ❌    |     ❌      |
| [cap.guru](https://cap.guru/ru)                                             |    ❌    |     ❌      |   ❌   |    ❌    |     ❌      |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |    ❌    |     ❌      |   ❌   |    ❌    |     ❌      |

## Supported Proxy types

| Service                                                                     | HTTP | HTTPS | SOCKS 4 | SOCKS 5 |
|-----------------------------------------------------------------------------|:----:|:-----:|:-------:|:-------:|
| [2captcha.com](http://2captcha.com/?from=12016127)	                         |  ✅   |   ✅   |    ✅    |    ✅    |
| [rucaptcha.com](https://rucaptcha.com?from=12016127)                        |  ✅   |   ✅   |    ✅    |    ✅    |
| [anti-captcha.com](http://getcaptchasolution.com/tmb2cervod)                |  ✅   |   ✅   |    ✅    |    ✅    |
| [azcaptcha.com](https://azcaptcha.com)                                      |  ✅   |   ✅   |    ✅    |    ✅    |
| [cap.guru](https://cap.guru/ru)                                             |  ✅   |   ✅   |    ✅    |    ✅    |
| [deathbycaptcha.com](https://deathbycaptcha.com/register?refid=6184199718b) |  ✅   |   ❌   |    ❌    |    ❌    |

## How to...

### Common

<details>
<summary>Get balance</summary>

```python
from anycaptcha import Solver, Service


async def main():
    async with Solver(Service.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        balance = await solver.get_balance()
        ...
```

</details>

<details>
<summary>Get service status (is the service is up?)</summary>

```python
from anycaptcha import Solver, Service


async def main():
    with Solver(Service.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # get status of the service (True - everything is Okay, False - probably the service is down)
        status = await solver.get_status()
        ...
```

</details>

<details>
<summary>Get technical details after solving</summary>

```python
from anycaptcha import Solver, Service


async def main():
    # init captcha solver and solve the captcha
    with Solver(Service.ANTI_CAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        solved = await solver.solve_...(...)

        # get cost of the solving
        cost = solved.cost

        # get cookies (if any)
        cookies = solved.cookies

        # report good captcha
        await solved.report_good()

        # report bad captcha
        await solved.report_bad()

        # get solving start time
        start_time = solved.start_time

        # get solving end time
        end_time = solved.end_time
```

</details>

### CAPTCHAs

<details>
<summary>Solve Image CAPTCHA</summary>

```python
from pathlib import Path

from anycaptcha import Solver, Service
from anycaptcha import CaptchaAlphabet
from anycaptcha import CaptchaCharType


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_image_captcha(
            image=Path('captcha.jpg'),  # it can be a Path, file-object or bytes.
            char_type=CaptchaCharType.ALPHA,  # optional
            is_phrase=False,  # optional
            is_case_sensitive=True,  # optional
            is_math=False,  # optional
            min_len=4,  # optional
            max_len=6,  # optional
            alphabet=CaptchaAlphabet.LATIN,  # optional
            comment='Type RED letters only'  # optional
        )
        # get CAPTCHA text
        token = solved.solution.text
```

</details>

<details>
<summary>Solve reCAPTCHA v2</summary>

```python
from anycaptcha import Solver, Service

# get page URL and site_key from your page
page_url = ...
site_key = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=page_url,
            data_s='<data-s value>',  # optional
            api_domain='<"google.com" or "recaptcha.net">'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve reCAPTCHA v2 Invisible</summary>

```python
from anycaptcha import Solver, Service

# get page url and site_key from your page
page_url = ...
site_key = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=page_url,
            is_invisible=True,
            data_s='<data-s value>',  # optional
            api_domain='<"google.com" or "recaptcha.net">'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve reCAPTCHA v2 Enterprise</summary>

```python
from anycaptcha import Solver, Service

# get page URL, site_key and data_s from your page
page_url = ...
site_key = ...
data_s = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=page_url,
            is_enterprise=True,
            data_s=data_s,  # optional
            api_domain='<"google.com" or "recaptcha.net">'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve reCAPTCHA v3</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...
action = ...
min_score = 0.7


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v3(
            site_key=site_key,
            page_url=page_url,
            action=action,  # optional
            min_score=min_score,  # optional
            api_domain='<"google.com" or "recaptcha.net">'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve reCAPTCHA v3 Enterprise</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...
action = ...
min_score = 0.7


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v3(
            site_key=site_key,
            page_url=page_url,
            is_enterprise=True,
            action=action,  # optional
            min_score=min_score,  # optional
            api_domain='<"google.com" or "recaptcha.net">'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve hCaptcha</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_hcaptcha(
            site_key=site_key,
            page_url=page_url,
            api_domain='< "hcaptcha.com" or "js.hcaptcha.com" >'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve hCaptcha Invisible</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
site_key = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_hcaptcha(
            site_key=site_key,
            page_url=page_url,
            is_invisible=True,
            api_domain='< "hcaptcha.com" or "js.hcaptcha.com" >'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve FunCaptcha</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
public_key = ...
page_url = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_funcaptcha(
            public_key=public_key,
            page_url=page_url,
            service_url='<value of surl parameter>',  # optional
            blob='<value of data[blob] parameter>'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve KeyCaptcha</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
user_id = ...
session_id = ...
ws_sign = ...
ws_sign2 = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_keycaptcha(
            page_url=page_url,
            user_id=user_id,
            session_id=session_id,
            ws_sign=ws_sign,
            ws_sign2=ws_sign2
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve Geetest</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
gt_key = ...
challenge = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_geetest(
            page_url=page_url,
            gt_key=gt_key,
            challenge=challenge,
            api_server='<value of api_server parameter>'  # optional
        )
        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Solve Geetest v4</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
page_url = ...
captcha_id = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_geetest_v4(
            page_url=page_url,
            captcha_id=captcha_id
        )

        # get solution data
        lot_number = solved.solution.lot_number
        pass_token = solved.solution.pass_token
        gen_time = solved.solution.gen_time
        captcha_output = solved.solution.captcha_output
```

</details>

<details>
<summary>Solve Capy Puzzle</summary>

```python
from anycaptcha import Solver, Service

# get CAPTCHA params from the target page/site
site_key = ...
page_url = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_capy_puzzle(
            site_key=site_key,
            page_url=page_url,
            api_server='<for example "https://api.capy.me">',  # optional
            challenge_type='<"puzzle" or "avatar">'  # optional
        )

        # get solution data
        captchakey = solved.solution.captchakey
        challengekey = solved.solution.challengekey
        answer = solved.solution.answer
```

</details>

<details>
<summary>Solve a text CAPTCHA</summary>

```python
from anycaptcha import Solver, Service
from anycaptcha import CaptchaAlphabet
from anycaptcha import WorkerLanguage


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_text_captcha(
            text='Si mañana es domingo, ¿qué día es hoy?',
            alphabet=CaptchaAlphabet.LATIN,  # optional
            language=WorkerLanguage.SPANISH  # optional
        )

        # get answer
        answer = solved.solution.text  # Sábado
```

</details>

### Error handling

<details>
<summary>Catch exceptions</summary>

```python
import anycaptcha
from anycaptcha import Solver, Service


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        try:
            solved = solver.solve_recaptcha_v2(
                site_key=site_key,
                page_url=page_url,
            )
        except anycaptcha.AccessDeniedError:  # wrong API key or the current IP is banned
            pass
        except anycaptcha.LowBalanceError:  # low balance
            pass
        except anycaptcha.ServiceTooBusy:  # no available slots to solve CAPTCHA
            pass
        except anycaptcha.SolutionWaitTimeout:  # haven't received a solution within N minutes
            pass
        except anycaptcha.TooManyRequestsError:  # request limit exceeded
            pass
        except anycaptcha.BadInputDataError:  # bad CAPTCHA data (bad image, wrong URL, etc.)
            pass
        except anycaptcha.UnableToSolveError:  # CAPTCHA unsolvable
            pass
        except anycaptcha.ProxyError:  # bad proxy
            pass
        else:
            # get response token
            token = solved.solution.token
```

</details>

### Misc

<details>
<summary>Create a task and wait for the result</summary>

```python
from anycaptcha import Solver, Service
from anycaptcha.captcha import RecaptchaV2

# get page URL and site_key from your page
page_url = ...
site_key = ...


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # create a task
        task = solver.create_task(
            RecaptchaV2(site_key, page_url)
        )

        # print task ID
        print(task.task_id)

        # wait for task to be completed
        solved = task.wait()

        # get response token
        token = solved.solution.token
```

</details>

<details>
<summary>Add proxy, cookies and User-Agent</summary>

```python
from anycaptcha import Solver, Service

# get page URL and site_key from your page
page_url = ...
site_key = ...
proxy = 'http://user:password@domain.com:8080'  # any format
user_agent = '<USER AGENT STRING>'
cookies = {'name': 'value', ...}


async def main():
    with Solver(Service.TWOCAPTCHA, "<PLACE YOUR API KEY HERE>") as solver:
        # solve CAPTCHA
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=page_url,
            proxy=proxy,
            user_agent=user_agent,
            cookies=cookies
        )
        # get response token
        token = solved.solution.token
```

</details>

from django.http import HttpResponse
import datetime

def set_cookies(response, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response = HttpResponse()
    response.set_cookie(
        key='student',
        value='001',
        max_age=max_age,
        expires=expires,
        domain=None,
        secure=None,
    )
    
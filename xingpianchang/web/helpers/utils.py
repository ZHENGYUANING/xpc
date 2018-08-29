from hashlib import md5
from django.conf import settings


def multi_encrypt(s, phone):
    if not phone:
        num = 10
    else:
        num = int(phone[-2:])
    for i in range(num):
        s = '%s%s' % (s, settings.SECRET_KEY)
        s = md5(s.encode('utf-8')).hexdigest()
    return s
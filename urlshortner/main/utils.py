from main.models import IncrementalNumber
from django.db.models import F

from collections import defaultdict

SHORT_URL_LENGTH = 7
CHARS_IN_URL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def get_incremental_number():
    inc_obj = IncrementalNumber.objects.all()[0]
    inc_num = inc_obj.short_url
    new_num = inc_num + 1
    inc_obj.short_url = new_num
    inc_obj.save()
    return new_num


class ShortUrl:
    short_to_long = defaultdict(str)
    long_to_short = defaultdict(str)

    @classmethod
    def generate_short_url(self, long_url):
        ShortUrl.counter = get_incremental_number()
        if long_url in ShortUrl.long_to_short:
            return ShortUrl.long_to_short[long_url]
        url = ShortUrl._base62(ShortUrl.counter)
        ShortUrl.long_to_short[long_url] = url
        ShortUrl.short_to_long[url] = long_url
        ShortUrl.counter += 1
        return url

    @classmethod
    def _base62(self, num):
        base_62 = ""
        while num:
            base_62 += CHARS_IN_URL[num % 62]
            num //= 62
        return base_62

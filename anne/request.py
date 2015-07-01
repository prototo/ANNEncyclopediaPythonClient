from time import time
from urllib.request import urlopen


redis = None
try:
    import redis as Redis
    redis = Redis.StrictRedis()
except:
    # no redis
    pass

def from_cache(func):
    def wrapper(url):
        if not redis:
            return func(url)
        try:
            redis.ping()
            cached = redis.get(url)
            if cached:
                return cached
            raise Exception('no cache for ' + url)
        except:
            response = func(url)
            redis.set(url, response)
            redis.expire(url, 84600)
            return response
    return wrapper

@from_cache
def get(url):
    return urlopen(url).read()


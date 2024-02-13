import redis
import time
from django.http import HttpResponse
from threading import Thread

# token bucket implementation
class RateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.rps = 1
        self.bucket_size = 10
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.thread = Thread(target=self._refill_tokens)
        self.thread.daemon = True
        self.thread.start()
        # self.clear_redis()
    
    def clear_redis(self):
        self.redis_client.flushdb()


    def _refill_tokens(self):
        try:
            while True:
                keys = self.redis_client.keys('*')
                print(keys)
                for key in keys:
                    if int(self.redis_client.hget(key, 'tokens')) < self.bucket_size:
                        self.redis_client.hset(key, 'tokens', int(self.redis_client.hget(key, 'tokens')) + self.rps)
                        self.redis_client.hset(key, 'last', int(time.time()))
                        print(self.redis_client.hget(key, 'tokens'))
                time.sleep(1)
                print("Thread finished")
        except Exception as e:
            print(f"Exception in thread: {e}")



    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        key = f'{client_ip}'
        current = self.redis_client.hget(key, 'tokens')
        print(current, key)
        #first time user
        if not self.redis_client.exists(key):
            self.redis_client.hset(key, 'tokens', self.bucket_size)
            current = self.bucket_size
            self.redis_client.hset(key, 'last', int(time.time()))
        if int(float(self.redis_client.hget(key, 'tokens'))) <= 0:
            return HttpResponse('Too many requests', status=429)
        
        self.redis_client.hset(key, 'tokens', int(float(self.redis_client.hget(key, 'tokens'))) - 1)
        
        return self.get_response(request)

    
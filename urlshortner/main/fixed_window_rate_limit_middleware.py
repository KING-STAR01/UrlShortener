import time
from django.http import HttpResponse
import redis


class FixedWindowMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.window_size = 1 #1 second
        self.capacity = 10
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    

    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        key = f'fixed_{client_ip}'
        print(key, self.redis_client.hget(key, 'tokens'))
        #add key if first time user
        if not self.redis_client.exists(key):
            self.redis_client.hset(key, 'tokens', 0)
            self.redis_client.hset(key, 'last', str(int(time.time())))
        
        #check if window has passed
        if int(time.time()) - int(self.redis_client.hget(key, 'last')) > self.window_size:
            self.redis_client.hset(key, 'tokens', 0)
            self.redis_client.hset(key, 'last', str(int(time.time())))
        
        #check if tokens are available
        if int(self.redis_client.hget(key, 'tokens')) >= self.capacity:
            return HttpResponse('Too many requests', status=429)
        
        #increment tokens
        self.redis_client.hset(key, 'tokens', int(self.redis_client.hget(key, 'tokens')) + 1)

        return self.get_response(request)
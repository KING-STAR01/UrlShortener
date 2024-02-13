import time
import json

import redis
from django.http import HttpResponse

class SlidingWindowRateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.window_size = 20
        self.rpws = 10



    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        key = f"sliding_{client_ip}"
# 
        #add key if first time user
        if not self.redis_client.exists(key):
            self.redis_client.rpush(key, int(time.time()))
            return self.get_response(request)


        while int(self.redis_client.lindex(key, 0)) <= int(time.time()) - self.window_size:
            self.redis_client.lpop(key)

        
        #check if tokens are available
        if self.redis_client.llen(key) >= self.rpws:
            return HttpResponse('Too many requests', status=429)
        
        #increment tokens
        self.redis_client.rpush(key, int(time.time()))

        return self.get_response(request)


import aiohttp
import asyncio
from time import perf_counter

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status

async def fetch_all(urls, loop):
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    url = ['http://127.0.0.1:8000/api/'] * 100
    start = perf_counter()
    responses = loop.run_until_complete(fetch_all(url, loop))
    end = perf_counter()
    print(f"Time taken: {end-start}")
    print(responses.count(429))

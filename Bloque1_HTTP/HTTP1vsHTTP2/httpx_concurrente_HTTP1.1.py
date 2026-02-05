import time
import asyncio
import httpx

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("httpcore.connection").setLevel(logging.DEBUG)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

URLS = [f"https://httpbin.org/bytes/1024?i={i}" for i in range(1, 11)]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

async def fetch(client, url, delay):
    await asyncio.sleep(delay)
    r = await client.get(url, headers=HEADERS)
    data = await r.aread()
    print(url, r.http_version, r.status_code, len(data))

async def main():
    async with httpx.AsyncClient(http2=False) as client:
        tasks = [fetch(client, url, delay=0.2 * i) for i, url in enumerate(URLS)]
        await asyncio.gather(*tasks)

start = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - start

print(f"Tiempo total (httpx, concurrente, HTTP/1.1): {elapsed:.3f} s")

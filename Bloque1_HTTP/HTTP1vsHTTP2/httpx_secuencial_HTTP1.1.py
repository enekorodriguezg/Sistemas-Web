import httpx
import time

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("httpcore.connection").setLevel(logging.DEBUG)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

URLS = [f"https://httpbin.org/bytes/1024?i={i}" for i in range(1, 11)]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

start = time.perf_counter()

with httpx.Client(http2=False, headers=HEADERS) as client:
    for i, url in enumerate(URLS):
        time.sleep(0.2 * i)
        r = client.get(url)
        print(url, r.http_version, r.status_code, len(r.content))

elapsed = time.perf_counter() - start

print(f"Tiempo total (httpx, secuencial, HTTP/1.1): {elapsed:.3f} s")

import os
import time
import urllib.request
import ssl
import threading
import statistics

TEST_DOWNLOAD_URL = "https://speed.hetzner.com/100MB.bin"
TEST_UPLOAD_URL = "https://httpbin.org/post"
UPLOAD_SIZE_BYTES = 1_000_000

def fetch_download(context, results):
    try:
        start = time.time()
        req = urllib.request.urlopen(TEST_DOWNLOAD_URL, context=context, timeout=15)
        total = 0
        while True:
            chunk = req.read(64 * 1024)
            if not chunk:
                break
            total += len(chunk)
        elapsed = time.time() - start
        mbps = (total * 8) / elapsed / 1e6
    except:
        mbps = 0.0
    results.append(round(mbps, 2))

def fetch_upload(context, results):
    try:
        data = os.urandom(UPLOAD_SIZE_BYTES)
        headers = {"Content-Type": "application/octet-stream"}
        start = time.time()
        req = urllib.request.Request(TEST_UPLOAD_URL, data=data, headers=headers, method="POST")
        resp = urllib.request.urlopen(req, context=context, timeout=15)
        resp.read()
        elapsed = time.time() - start
        mbps = (UPLOAD_SIZE_BYTES * 8) / elapsed / 1e6
    except:
        mbps = 0.0
    results.append(round(mbps, 2))

def run(duration):
    ssl_context = ssl._create_unverified_context()
    dl = []
    ul = []
    end = time.time() + duration

    while time.time() < end:
        dl_result = []
        ul_result = []
        threads = []

        for _ in range(2):
            d = threading.Thread(target=fetch_download, args=(ssl_context, dl_result))
            u = threading.Thread(target=fetch_upload, args=(ssl_context, ul_result))
            threads.append(d)
            threads.append(u)
            d.start()
            u.start()

        for t in threads:
            t.join()

        dl.extend(dl_result)
        ul.extend(ul_result)

    return {
        "download_avg": round(statistics.mean(dl), 2) if dl else 0.0,
        "download_min": round(min(dl), 2) if dl else 0.0,
        "download_max": round(max(dl), 2) if dl else 0.0,
        "upload_avg": round(statistics.mean(ul), 2) if ul else 0.0,
        "upload_min": round(min(ul), 2) if ul else 0.0,
        "upload_max": round(max(ul), 2) if ul else 0.0
    }

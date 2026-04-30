import time
import requests
import statistics

BASE = "http://127.0.0.1:8000"
ENDPOINTS = ["/", "/api/personality/health"]
NUM = 30

results = {}
for ep in ENDPOINTS:
    latencies = []
    url = BASE + ep
    for i in range(NUM):
        t0 = time.perf_counter()
        try:
            r = requests.get(url, timeout=10)
            ok = r.status_code
        except Exception as e:
            ok = None
        t1 = time.perf_counter()
        lat = (t1 - t0) * 1000.0
        latencies.append(lat)
    latencies_sorted = sorted(latencies)
    results[ep] = {
        "count": NUM,
        "min_ms": min(latencies_sorted),
        "avg_ms": statistics.mean(latencies_sorted),
        "median_ms": statistics.median(latencies_sorted),
        "p95_ms": latencies_sorted[int(len(latencies_sorted)*0.95)-1],
        "p99_ms": latencies_sorted[int(len(latencies_sorted)*0.99)-1] if len(latencies_sorted)>1 else latencies_sorted[-1],
    }

print("API benchmark results:")
for ep, stats in results.items():
    print(ep, stats)

import statistics

def evaluate(pings, duration, speed):
    received = len([p for p in pings if p is not None])
    loss = round((1 - received / duration) * 100, 2)
    valid_pings = [p for p in pings if p]
    avg = round(statistics.mean(valid_pings), 2) if valid_pings else 0
    jitter = round(statistics.stdev(valid_pings), 2) if len(valid_pings) > 1 else 0

    stable_dl = speed["download_avg"] >= 3 and (speed["download_max"] - speed["download_min"]) / max(speed["download_avg"], 1) <= 0.5
    stable_ul = speed["upload_avg"] >= 2 and (speed["upload_max"] - speed["upload_min"]) / max(speed["upload_avg"], 1) <= 0.5
    stable_ping = avg <= 50 and jitter <= 15 and loss <= 2

    status = "✅ STABLE" if stable_dl and stable_ul and stable_ping else "⚠️ UNSTABLE"

    return {
        "status": status,
        "avg": avg,
        "min": round(min(valid_pings), 2) if valid_pings else 0,
        "max": round(max(valid_pings), 2) if valid_pings else 0,
        "jitter": jitter,
        "loss": loss,
        "speed": speed
    }

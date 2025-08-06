import datetime

def log(result):
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"network_log_{ts}.txt"
    with open(filename, "w") as f:
        f.write(f"STATUS: {result['status']}\n")
        f.write(f"Ping avg/min/max: {result['avg']} / {result['min']} / {result['max']} ms\n")
        f.write(f"Jitter: {result['jitter']} ms\n")
        f.write(f"Packet loss: {result['loss']}%\n")
        f.write(f"Download avg/min/max: {result['speed']['download_avg']} / {result['speed']['download_min']} / {result['speed']['download_max']} Mbps\n")
        f.write(f"Upload avg/min/max: {result['speed']['upload_avg']} / {result['speed']['upload_min']} / {result['speed']['upload_max']} Mbps\n")
    return filename

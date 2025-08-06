import subprocess, platform, time

def run(host, duration):
    cmd = ["ping", "-n" if platform.system() == "Windows" else "-c", "1", host]
    pings, end = [], time.time() + duration
    try:
        while time.time() < end:
            output = subprocess.check_output(cmd).decode()
            ms = float(output.split('time=')[1].split()[0].replace('ms',''))
            pings.append(ms)
            yield ms
            time.sleep(1)
    except subprocess.CalledProcessError:
        yield None
    finally:
        return pings

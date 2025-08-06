from ping_test import run as pingtest
from evaluator import evaluate
from speed_test import run as speedtest
from logger import log
import time

def main():
    print("\nNET-DIAGNOSTICS FOR MICROSOFT TEAMS")
    print("\nThis tool tests the STABILITY of your internet connection.")
    print("You will specify a duration in seconds.")
    print("That duration will apply to EACH TEST PHASE (speed + ping).")
    print("Example: 30 means 30s speed test + 30s ping test.\n")

    duration = input("Enter duration per test (default 180): ")
    duration = int(duration) if duration.isdigit() else 180
    input("\nPress Enter to start the tests...")

    print("\nRunning speed test...\n")
    speed = speedtest(duration)
    print(f"Download avg: {speed['download_avg']} Mbps")
    print(f"Upload avg: {speed['upload_avg']} Mbps\n")

    print("Running ping test to teams.microsoft.com...\n")
    pings, start_time = [], time.time()

    try:
        for ms in pingtest('teams.microsoft.com', duration):
            if ms is not None:
                print(f"Ping: {ms} ms")
                pings.append(ms)
            else:
                print("Timeout")
    except KeyboardInterrupt:
        print("\nTest aborted by user.")

    actual_duration = max(int(time.time() - start_time), 1)
    result = evaluate(pings, actual_duration, speed)

    print(f"\nRESULT: {result['status']}")
    print(f"Ping: avg {result['avg']} ms | min {result['min']} ms | max {result['max']} ms")
    print(f"Jitter: {result['jitter']} ms | Loss: {result['loss']}%")
    print(f"Download avg: {speed['download_avg']} Mbps (min: {speed['download_min']} / max: {speed['download_max']})")
    print(f"Upload avg: {speed['upload_avg']} Mbps (min: {speed['upload_min']} / max: {speed['upload_max']})\n")

    logfile = log(result)
    print(f"Log saved to {logfile}\n")

    if input("Run again? [y/N]: ").lower() == 'y':
        main()

if __name__ == "__main__":
    main()

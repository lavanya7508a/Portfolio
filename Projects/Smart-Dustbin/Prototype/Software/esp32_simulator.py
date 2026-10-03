"""
ESP32 + HC-SR04 Hardware Telemetry Simulator
Simulates physical ultrasonic sensor distance measurements and sends HTTP POST
telemetry payloads to the Smart Dustbin Flask server.

Ultrasonic Formula:
Distance (cm) = (Pulse Time * 0.0343) / 2
Fill % = ((Bin Height - Distance) / Bin Height) * 100
"""

import sys
import time
import random
import urllib.request
import json
import argparse


def send_telemetry(server_url, bin_id, fill_pct, battery_pct=94):
    url = f"{server_url.rstrip('/')}/api/bins/{bin_id}/reading"
    distance_cm = round(100.0 - fill_pct, 1)
    payload = {
        "fill_pct": round(fill_pct, 1),
        "distance_cm": distance_cm,
        "battery_pct": battery_pct,
        "device": "ESP32-WROOM-32",
        "sensor": "HC-SR04-Ultrasonic"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return True, res_data
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="ESP32 Ultrasonic Telemetry Simulator")
    parser.add_argument("--server", default="http://127.0.0.1:5000", help="Backend server URL")
    parser.add_argument("--bin", default="BIN-001", help="Target Dustbin ID (BIN-001 to BIN-004)")
    parser.add_argument("--fill", type=float, default=None, help="Set specific fill percentage (0-100)")
    parser.add_argument("--continuous", action="store_true", help="Run continuous simulation loop")
    parser.add_argument("--interval", type=int, default=3, help="Interval in seconds for continuous mode")

    args = parser.parse_args()

    print("=================================================================")
    print("  ESP32 + HC-SR04 Ultrasonic Telemetry Hardware Simulator")
    print(f"  Target: {args.server} | Dustbin: {args.bin}")
    print("=================================================================")

    if args.fill is not None:
        print(f"[*] Setting {args.bin} fill level to {args.fill}%...")
        ok, res = send_telemetry(args.server, args.bin, args.fill)
        if ok:
            print(f"[+] Success: Status={res.get('bin', {}).get('status')}, Distance={res.get('bin', {}).get('sensor_distance_cm')}cm")
        else:
            print(f"[-] Failed to send telemetry: {res}")
        return

    if args.continuous:
        print(f"[*] Starting continuous simulation loop (interval: {args.interval}s)...")
        print("Press Ctrl+C to stop.")
        current_fill = 65.0
        battery = 95

        while True:
            # Simulate waste accumulation
            step = random.choice([1.5, 2.5, 4.0, 5.5])
            current_fill = min(100.0, current_fill + step)
            dist = round(100.0 - current_fill, 1)

            print(f"[TX] Ultrasonic Ping -> Distance: {dist}cm | Fill: {current_fill:.1f}% | Battery: {battery}%")
            ok, res = send_telemetry(args.server, args.bin, current_fill, battery)

            if ok:
                b_info = res.get("bin", {})
                status = b_info.get("status", "Normal")
                flag = "[ALERT TRIGGERED]" if status in ("Warning", "Overflow") else "[OK]"
                print(f"   ↳ Response: HTTP 200 {flag} Status: {status}")
            else:
                print(f"   ↳ Transmission Error: {res}")

            if current_fill >= 100.0:
                print("\n[!] Bin reached 100% capacity! Simulating emptying cycle in 5 seconds...\n")
                time.sleep(5)
                current_fill = 0.0
                send_telemetry(args.server, args.bin, 0.0, battery)
                print("[*] Bin cleared! Fill reset to 0%.\n")

            time.sleep(args.interval)
    else:
        # One-off burst test across all 4 bins
        print("[*] Executing test telemetry burst across all 4 Goundanur bins:")
        test_levels = [
            ("BIN-001", 86.0),
            ("BIN-002", 96.0),
            ("BIN-003", 48.0),
            ("BIN-004", 72.0),
        ]
        for bid, lvl in test_levels:
            ok, res = send_telemetry(args.server, bid, lvl)
            stat = res.get("bin", {}).get("status") if ok else "ERR"
            print(f"  • {bid}: Fill={lvl}% -> Server Status={stat}")

        print("\nSimulator burst complete. Run with --continuous to simulate live sensor stream.")


if __name__ == "__main__":
    main()
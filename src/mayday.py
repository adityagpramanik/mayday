#!/usr/bin/env python3
import time
import subprocess
from datetime import datetime

THRESHOLD = 97  # percent
SLEEP_SECONDS = 2

# ---------------------------------------
# HARD-CODED DRY RUN FLAG
# Set to True for testing (no shutdown)
# ---------------------------------------
DRY_RUN = False
# ---------------------------------------

# -------- Local helpers ----------
def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------- CPU helpers ----------
def read_cpu_totals():
    with open("/proc/stat", "r") as f:
        line = f.readline().split()
    vals = [int(x) for x in line[1:9]]
    user, nice, system, idle, iowait, irq, softirq, steal = (vals + [0]*8)[:8]
    idle_all = idle + iowait
    non_idle = user + nice + system + irq + softirq + steal
    total = idle_all + non_idle
    return total, idle_all


def cpu_percent(prev_total, prev_idle, cur_total, cur_idle):
    total_delta = cur_total - prev_total
    idle_delta = cur_idle - prev_idle
    if total_delta <= 0:
        return 0.0
    usage = (1.0 - idle_delta / total_delta) * 100.0
    return max(0.0, min(usage, 100.0))


# ---------- MEMORY + SWAP ----------
def mem_swap_percent():
    mem_total = mem_available = swap_total = swap_free = 0
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                mem_available = int(line.split()[1])
            elif line.startswith("SwapTotal:"):
                swap_total = int(line.split()[1])
            elif line.startswith("SwapFree:"):
                swap_free = int(line.split()[1])

    mem_used_pct = (1 - mem_available / mem_total) * 100.0 if mem_total else 0.0
    swap_used_pct = (1 - swap_free / swap_total) * 100.0 if swap_total else 0.0
    return (mem_used_pct + swap_used_pct) / 2.0


# ---------- TEMPERATURE ----------
def get_temp():
    sys_temp_path = "/sys/class/thermal/thermal_zone0/temp"
    if DRY_RUN:
       sys_temp_path = "/tmp/fake_temp" 
    try:
        with open(sys_temp_path, "r") as f:
            return int(f.read().strip()) / 1000.0
    except Exception:
        return 0.0


# ---------- MAIN CHECK ----------
def check_and_shutdown(cpu_usage, memswap, temp_c):
    print(f"{ts()} CPU={cpu_usage:.1f}%, MEM+SWAP={memswap:.1f}%, TEMP={temp_c:.1f}°C {'DRY_RUN=True' if DRY_RUN else ''}", flush=True)

    if cpu_usage > THRESHOLD or memswap > THRESHOLD or temp_c > THRESHOLD:
        if DRY_RUN:
            print(f"{ts()} 🧪 DRY RUN: Threshold crossed — would shutdown now!", flush=True)
        else:
            print(f"{ts()} ⚠️ Threshold crossed — shutting down immediately!", flush=True)
            subprocess.run(["sudo", "shutdown", "-f", "now"])


def main():
    prev_total, prev_idle = read_cpu_totals()

    if DRY_RUN:
        print("🔧 DRY RUN ENABLED — script will NOT shutdown the Pi.", flush=True)

    while True:
        cur_total, cur_idle = read_cpu_totals()
        cpu_usage = cpu_percent(prev_total, prev_idle, cur_total, cur_idle)
        prev_total, prev_idle = cur_total, cur_idle

        memswap = mem_swap_percent()
        temp_c = get_temp()

        check_and_shutdown(cpu_usage, memswap, temp_c)
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
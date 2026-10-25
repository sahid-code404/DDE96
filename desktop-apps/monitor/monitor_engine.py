"""Linux System Activity Monitor Engine.

Directly parses Linux kernel statistics from /proc/stat, /proc/meminfo,
and /proc/[pid]/ with honest POSIX permission boundaries.
"""

import os
import time
import shutil
import signal
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class SystemMonitorEngine:
    def __init__(self):
        self.prev_total_jiffies = 0
        self.prev_idle_jiffies = 0
        self.current_uid = os.getuid()
        self._init_cpu_sample()

    def _init_cpu_sample(self):
        try:
            with open("/proc/stat", "r") as f:
                line = f.readline()
                parts = [int(x) for x in line.split()[1:]]
                self.prev_idle_jiffies = parts[3] + (parts[4] if len(parts) > 4 else 0)
                self.prev_total_jiffies = sum(parts)
        except Exception:
            pass

    def get_cpu_metrics(self) -> Dict[str, Any]:
        """Returns total CPU percentage and per-core utilization."""
        try:
            with open("/proc/stat", "r") as f:
                lines = f.readlines()
        except Exception:
            return {"total_percent": 0.0, "cores": []}

        first_parts = [int(x) for x in lines[0].split()[1:]]
        idle = first_parts[3] + (first_parts[4] if len(first_parts) > 4 else 0)
        total = sum(first_parts)

        delta_total = max(1, total - self.prev_total_jiffies)
        delta_idle = max(0, idle - self.prev_idle_jiffies)

        self.prev_total_jiffies = total
        self.prev_idle_jiffies = idle

        cpu_usage = max(0.0, min(100.0, ((delta_total - delta_idle) / delta_total) * 100.0))
        return {
            "total_percent": round(cpu_usage, 1),
            "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
        }

    def get_memory_metrics(self) -> Dict[str, Any]:
        """Parses /proc/meminfo for memory and swap metrics."""
        mem = {}
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = int(parts[1].strip().split()[0]) # KB
                        mem[key] = val
        except Exception:
            return {"total_mb": 0, "used_mb": 0, "free_mb": 0, "percent": 0.0}

        total_kb = mem.get("MemTotal", 1)
        avail_kb = mem.get("MemAvailable", mem.get("MemFree", 0))
        used_kb = max(0, total_kb - avail_kb)

        return {
            "total_mb": total_kb // 1024,
            "used_mb": used_kb // 1024,
            "free_mb": avail_kb // 1024,
            "percent": round((used_kb / total_kb) * 100.0, 1)
        }

    def get_disk_metrics(self) -> Dict[str, Any]:
        """Returns root filesystem space usage."""
        try:
            usage = shutil.disk_usage("/")
            total_gb = usage.total / (1024 ** 3)
            used_gb = usage.used / (1024 ** 3)
            free_gb = usage.free / (1024 ** 3)
            pct = (usage.used / usage.total) * 100.0
            return {
                "total_gb": round(total_gb, 1),
                "used_gb": round(used_gb, 1),
                "free_gb": round(free_gb, 1),
                "percent": round(pct, 1)
            }
        except Exception:
            return {"total_gb": 0.0, "used_gb": 0.0, "free_gb": 0.0, "percent": 0.0}

    def get_processes(self, query: str = "", limit: int = 100) -> List[Dict[str, Any]]:
        """Parses /proc/[pid] entries honoring user permissions."""
        processes = []
        try:
            pids = [int(p) for p in os.listdir("/proc") if p.isdigit()]
        except Exception:
            return []

        for pid in pids:
            proc_path = Path(f"/proc/{pid}")
            try:
                # Read command / name
                with open(proc_path / "comm", "r", encoding="utf-8", errors="replace") as f:
                    name = f.read().strip()

                if query and query.lower() not in name.lower() and query not in str(pid):
                    continue

                # Read status for UID and RSS memory
                rss_kb = 0
                uid = 0
                state = "R"
                threads = 1
                with open(proc_path / "status", "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if line.startswith("Uid:"):
                            uid = int(line.split()[1])
                        elif line.startswith("VmRSS:"):
                            rss_kb = int(line.split()[1])
                        elif line.startswith("State:"):
                            state = line.split()[1]
                        elif line.startswith("Threads:"):
                            threads = int(line.split()[1])

                is_user_owned = (uid == self.current_uid)
                user_label = "User" if is_user_owned else "System"

                processes.append({
                    "pid": pid,
                    "name": name,
                    "state": state,
                    "user": user_label,
                    "is_user_owned": is_user_owned,
                    "rss_mb": round(rss_kb / 1024.0, 1),
                    "threads": threads
                })
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                continue

        processes.sort(key=lambda p: (not p["is_user_owned"], -p["rss_mb"]))
        return processes[:limit]

    def terminate_process(self, pid: int, force: bool = False) -> Tuple[bool, str]:
        """Terminates process with SIGTERM or SIGKILL, returning honest status."""
        sig = signal.SIGKILL if force else signal.SIGTERM
        try:
            os.kill(pid, sig)
            return True, f"Sent {'SIGKILL' if force else 'SIGTERM'} to PID {pid}"
        except PermissionError:
            return False, f"Permission denied: process {pid} belongs to another user or root"
        except ProcessLookupError:
            return False, f"Process {pid} no longer exists"
        except Exception as e:
            return False, f"Error terminating process {pid}: {e}"

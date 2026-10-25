"""Unit tests for System Activity Monitor procfs parsing and honest permissions."""

import os
import unittest
from pathlib import Path

# Add project root and monitor dir
PROJECT_ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(PROJECT_ROOT / "desktop-apps" / "monitor"))

from monitor_engine import SystemMonitorEngine

class TestSystemMonitor(unittest.TestCase):
    def setUp(self):
        self.engine = SystemMonitorEngine()

    def test_cpu_metrics_bounds(self):
        metrics = self.engine.get_cpu_metrics()
        self.assertIn("total_percent", metrics)
        self.assertGreaterEqual(metrics["total_percent"], 0.0)
        self.assertLessEqual(metrics["total_percent"], 100.0)

    def test_memory_metrics_bounds(self):
        mem = self.engine.get_memory_metrics()
        self.assertGreater(mem["total_mb"], 0)
        self.assertGreaterEqual(mem["used_mb"], 0)
        self.assertLessEqual(mem["used_mb"], mem["total_mb"])
        self.assertGreaterEqual(mem["percent"], 0.0)
        self.assertLessEqual(mem["percent"], 100.0)

    def test_disk_metrics_bounds(self):
        disk = self.engine.get_disk_metrics()
        self.assertGreater(disk["total_gb"], 0.0)
        self.assertGreaterEqual(disk["used_gb"], 0.0)
        self.assertLessEqual(disk["used_gb"], disk["total_gb"])
        self.assertGreaterEqual(disk["percent"], 0.0)
        self.assertLessEqual(disk["percent"], 100.0)

    def test_process_enumeration(self):
        procs = self.engine.get_processes(limit=20)
        self.assertGreater(len(procs), 0)
        for p in procs:
            self.assertIn("pid", p)
            self.assertIn("name", p)
            self.assertIn("user", p)
            self.assertIn(p["user"], ["User", "System"])
            self.assertIsInstance(p["is_user_owned"], bool)

    def test_honest_permission_enforcement(self):
        # Attempting to signal PID 1 should fail honestly for unprivileged user
        if os.getuid() != 0:
            success, msg = self.engine.terminate_process(1, force=False)
            self.assertFalse(success)
            self.assertTrue("Permission denied" in msg or "no longer exists" in msg)

if __name__ == "__main__":
    unittest.main()

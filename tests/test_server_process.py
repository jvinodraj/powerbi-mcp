import os
import sys
import time
import subprocess


def test_server_stays_running():
    env = os.environ.copy()
    env.setdefault("MCP_PERSIST", "1")
    proc = subprocess.Popen([
        sys.executable,
        os.path.join("src", "server.py"),
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    try:
        time.sleep(2)
        # Process should still be running after 2 seconds
        assert proc.poll() is None
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


import os
import re
import signal
import subprocess
import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="OCI ARM Catcher Dashboard API", version="1.0.0")

# Enable CORS for Vercel and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HOME = Path.home()
CATCHER_DIR = HOME / "catcher"
CATCHER_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = CATCHER_DIR / "catcher.log"
PID_FILE = CATCHER_DIR / "catcher.pid"
EXE_PATH = HOME / ".cargo" / "bin" / "oci-arm-catcher"
CONFIG_PATH = HOME / ".oci" / "config"
SSH_PUB_PATH = HOME / ".oci" / "ssh-key.pub"

# Secret API Key to protect the endpoints
API_KEY = os.environ.get("DASHBOARD_API_KEY", "quanglab-secret-2026")

LAUNCH_ARGS = [
    str(EXE_PATH),
    "--compartment-id", "ocid1.tenancy.oc1..aaaaaaaaygucguze6omjz65lvk7pdjsdr2habcpvrevcm5ruhhjv7nkqrivq",
    "--availability-domains", "KmOT:AP-OSAKA-1-AD-1",
    "--subnet-id", "ocid1.subnet.oc1.ap-osaka-1.aaaaaaaanre6d7q24ivllvb5v4ojrkbfxf74ticar6i62getx3rvvv2cthjq",
    "--image-id", "ocid1.image.oc1.ap-osaka-1.aaaaaaaaepqpk4uqvhreavmhywycsiiqvok5ppvdfqjntb4tpckpopdyhxtq",
    "--ssh-key-file", str(SSH_PUB_PATH),
    "--display-name", "quanglab-vps",
    "--ocpus", "2",
    "--memory-gb", "12",
    "--boot-volume-gb", "100",
    "--retry-interval", "150"
]

def verify_token(x_api_key: Optional[str] = Header(None), key: Optional[str] = Query(None)):
    token = x_api_key or key
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return token

def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False

def get_catcher_pid() -> Optional[int]:
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if is_process_running(pid):
                return pid
        except Exception:
            pass
    # Fallback to pgrep
    try:
        out = subprocess.check_output(["pgrep", "-f", "oci-arm-catcher"], text=True)
        pids = [int(p) for p in out.strip().split() if p.isdigit()]
        if pids:
            return pids[0]
    except Exception:
        pass
    return None

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/status")
def get_status(_: str = Depends(verify_token)):
    pid = get_catcher_pid()
    running = pid is not None
    
    attempts = 0
    success = False
    instance_id = None
    last_line = ""
    last_status = "Chưa có lượt chạy"
    
    if LOG_FILE.exists():
        try:
            lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
            if lines:
                last_line = lines[-1]
                # Look for attempt numbers
                for line in reversed(lines):
                    m = re.search(r"Attempt #(\d+)", line)
                    if m:
                        attempts = int(m.group(1))
                        break
                # Look for success
                for line in reversed(lines):
                    m_succ = re.search(r"SUCCESS! Instance created:\s*(ocid1\.instance\.[A-Za-z0-9._-]+)", line)
                    if m_succ:
                        success = True
                        instance_id = m_succ.group(1)
                        break
                # Parse last status message
                for line in reversed(lines):
                    if "Out of host capacity" in line:
                        last_status = "Out of host capacity (500)"
                        break
                    elif "SUCCESS" in line:
                        last_status = "SUCCESS! Đã tạo thành công"
                        break
                    elif "Error" in line:
                        last_status = line.strip()
                        break
        except Exception as e:
            last_status = f"Lỗi đọc log: {str(e)}"

    return {
        "running": running,
        "pid": pid,
        "attempts": attempts,
        "success": success,
        "instance_id": instance_id,
        "last_status": last_status,
        "last_line": last_line,
        "interval_seconds": 150,
        "specs": {
            "name": "quanglab-vps",
            "region": "ap-osaka-1",
            "ad": "AD-1",
            "shape": "VM.Standard.A1.Flex",
            "ocpus": 2,
            "memory_gb": 12,
            "boot_gb": 100
        }
    }

@app.get("/api/logs")
def get_logs(lines: int = 100, _: str = Depends(verify_token)):
    if not LOG_FILE.exists():
        return {"logs": ["Log file does not exist yet."]}
    try:
        content = LOG_FILE.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
        tail = content[-lines:] if len(content) > lines else content
        return {"logs": tail}
    except Exception as e:
        return {"logs": [f"Error reading log file: {str(e)}"]}

@app.post("/api/start")
def start_catcher(_: str = Depends(verify_token)):
    pid = get_catcher_pid()
    if pid:
        return {"message": "Catcher is already running", "pid": pid}
    
    if not EXE_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Binary not found at {EXE_PATH}")
    if not CONFIG_PATH.exists():
        raise HTTPException(status_code=500, detail=f"OCI config not found at {CONFIG_PATH}")
    if not SSH_PUB_PATH.exists():
        raise HTTPException(status_code=500, detail=f"SSH public key not found at {SSH_PUB_PATH}")

    log_fh = open(LOG_FILE, "a", encoding="utf-8")
    proc = subprocess.Popen(
        LAUNCH_ARGS,
        cwd=str(CATCHER_DIR),
        stdout=log_fh,
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    PID_FILE.write_text(str(proc.pid))
    return {"message": "Catcher started successfully", "pid": proc.pid}

@app.post("/api/stop")
def stop_catcher(_: str = Depends(verify_token)):
    pid = get_catcher_pid()
    if not pid:
        return {"message": "Catcher is not running"}
    try:
        os.kill(pid, signal.SIGTERM)
        if PID_FILE.exists():
            PID_FILE.unlink(missing_ok=True)
        return {"message": f"Sent SIGTERM to process {pid}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop process {pid}: {str(e)}")

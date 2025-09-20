import os
import subprocess


def run_exporter(synopsis: str) -> subprocess.CompletedProcess:
    script_path = os.getenv("SCRIPT_PATH")
    script_dir = os.getenv("SCRIPT_DIRECTORY")


    if not script_path or not script_dir:
        raise RuntimeError("SCRIPT_PATH et SCRIPT_DIRECTORY doivent être définis")


    cmd: list[str] = ["python", script_path, "--synopsis", synopsis]
    return subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True, check=False)

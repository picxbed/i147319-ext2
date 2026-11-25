import os, subprocess
hdr = "===I147319-PROOF===\n"
if os.name == "nt":
    tmp = os.environ.get("TEMP", r"C:\Windows\Temp")
    bat = os.path.join(tmp, "i147319_probe.bat")
    outp = os.path.join(tmp, "i147319_out.txt")
    lines = [
        "@echo off",
        "echo ==== whoami ====",
        "whoami /user",
        "whoami",
        "echo ==== host ====",
        "hostname",
        "echo ==== where ====",
        "where nvidia-smi",
        'if exist "C:\\Windows\\System32\\nvidia-smi.exe" echo FOUND_SYSTEM32',
        'if exist "C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" echo FOUND_NVSMI',
        "echo ==== smi-system32 ====",
        '"C:\\Windows\\System32\\nvidia-smi.exe" -L 2>&1',
        '"C:\\Windows\\System32\\nvidia-smi.exe" --query-gpu=name,uuid,memory.total,memory.free,driver_version --format=csv,noheader 2>&1',
        "echo ==== smi-nvsmi ====",
        '"C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" -L 2>&1',
        '"C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe" --query-gpu=name,uuid,memory.total,memory.free,driver_version --format=csv,noheader 2>&1',
        "echo ==== smi-path ====",
        "nvidia-smi -L 2>&1",
        "echo ==== wmic ====",
        'wmic path win32_VideoController get name 2>&1',
        "echo ==== end ====",
    ]
    try:
        open(bat, "w").write("\r\n".join(lines) + "\r\n")
    except Exception:
        pass
    try:
        with open(outp, "w") as f:
            subprocess.run(["cmd", "/c", bat], stdout=f, stderr=subprocess.STDOUT, timeout=150)
    except Exception as e:
        try:
            open(outp, "w").write("RUN-EXC " + repr(e))
        except Exception:
            pass
    data = ""
    try:
        data = open(outp, "r", errors="replace").read()
    except Exception as e:
        data = "READ-EXC " + repr(e)
    for p in [os.path.join(os.path.expanduser("~"), "i147319_proof.txt"),
              os.path.join(tmp, "i147319_proof.txt")]:
        try:
            open(p, "w").write(hdr + data)
        except Exception:
            pass
else:
    cmd = ('nvidia-smi -L; nvidia-smi --query-gpu=name,uuid,memory.total,memory.free,'
           'driver_version --format=csv,noheader; hostname; id')
    try:
        data = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90).stdout
    except Exception as e:
        data = "ERR " + repr(e)
    for p in ["/app/i147319_proof.txt", "/tmp/i147319_proof.txt"]:
        try:
            open(p, "w").write(hdr + data)
        except Exception:
            pass
print(hdr + data)

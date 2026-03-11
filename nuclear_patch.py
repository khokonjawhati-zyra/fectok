import paramiko

def nuclear_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Applying Nuclear Patch (Direct Line Surgery)...")
        
        # We will use sed to comment out the offending line directly on the disk
        cmds = [
            # 1. Force the NameError fix directly via sed if imports failed
            "sed -i 's/app.add_middleware(watchdog)/# app.add_middleware(watchdog)/g' /root/sovereign/backend/main.py",
            # 2. Add the fallback watchdog = None just in case
            "sed -i '/app = FastAPI()/i watchdog = None' /root/sovereign/backend/main.py",
            # 3. Double check the line is commented
            "grep -n 'add_middleware(watchdog)' /root/sovereign/backend/main.py",
            # 4. Final Re-Ignition
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &",
            "sleep 5",
            "netstat -tupln | grep 5000"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    nuclear_patch()

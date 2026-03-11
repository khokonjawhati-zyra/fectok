import paramiko

def inject_missing():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Injecting missing dependencies (httpx, etc.) into VENV...")
        
        cmds = [
            "/root/sovereign/backend/venv/bin/pip install httpx jinja2 aiofiles",
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup /root/sovereign/backend/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &",
            "sleep 5"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            ssh.exec_command(c)
            # wait for execution
            
        print("Update pulses sent. Port 5000 should be live in 10 seconds.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inject_missing()

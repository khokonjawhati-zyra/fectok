import paramiko

def force_inject():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Forcing system-wide dependency injection...")
        
        # apt-get is safer for system modules on newer Ubuntu
        cmds = [
            "apt-get update",
            "apt-get install -y python3-fastapi python3-motor python3-websockets python3-multipart python3-requests",
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &",
            "sleep 5"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            ssh.exec_command(c)
            # No sleep here, let them queue or use blocking calls if needed
            
        print("Injection request sent. Wait 10 seconds and then check status.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_inject()

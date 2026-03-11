import paramiko

def sync_inject():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Forcing synchronous VENV update...")
        
        # Combined install for speed and correctness
        cmd = "/root/sovereign/backend/venv/bin/pip install fastapi uvicorn[standard] motor websockets python-multipart requests httpx jinja2 aiofiles"
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        print(f"Install status: {exit_status}")
        
        print("Igniting Engine...")
        launch = "pkill -f uvicorn || true; cd /root/sovereign/backend && nohup /root/sovereign/backend/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &"
        ssh.exec_command(launch)
        
        print("Waiting for boot...")
        import time
        time.sleep(5)
        
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep 5000")
        listen = stdout.read().decode().strip()
        print(f"Listen Status: {listen}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_inject()

import paramiko
import time

def reconstruct_venv():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Reconstructing VENV at /root/sovereign/backend/venv...")
        
        cmds = [
            # 1. Ensure venv is created inside the backend folder
            "cd /root/sovereign/backend && python3 -m venv venv",
            # 2. Install EVERYTHING in one go
            "/root/sovereign/backend/venv/bin/pip install fastapi uvicorn[standard] motor websockets python-multipart requests httpx jinja2 aiofiles",
            # 3. Kill and Launch
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            exit_status = stdout.channel.recv_exit_status()
            print(f"Exit status: {exit_status}")
            
        print("Waiting 5s for port activation...")
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep 5000")
        listen = stdout.read().decode().strip()
        print(f"RESULT: {listen}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reconstruct_venv()

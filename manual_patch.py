import paramiko

def manual_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Forcing manual patch of main.py...")
        
        sftp = ssh.open_sftp()
        sftp.put("backend/main.py", "/root/sovereign/backend/main.py")
        sftp.close()
        
        print("Patch applied. Attempting restart...")
        launch = "pkill -f uvicorn || true; cd /root/sovereign/backend && nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &"
        ssh.exec_command(launch)
        
        print("Wait 5s...")
        import time
        time.sleep(5)
        
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep 5000")
        print(f"Listen Status: {stdout.read().decode()}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    manual_patch()

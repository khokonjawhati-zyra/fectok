import paramiko

def inject_deps():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Injecting critical dependencies system-wide...")
        
        cmds = [
            "apt-get update && apt-get install -y python3-pip python3-uvicorn python3-full",
            "pip3 install fastapi uvicorn[standard] motor websockets python-multipart --break-system-packages",
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 5000 --break-system-packages > backend.log 2>&1 &"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Use channel to wait for output and exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Exit status: {exit_status}")
            
        print("INJECTION COMPLETE. CHECKING PORT 5000...")
        ssh.exec_command("sleep 5")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep 5000")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inject_deps()

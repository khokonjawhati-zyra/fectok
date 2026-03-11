import paramiko

def force_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    # Path to local file we just edited
    local_file = "backend/main.py"
    remote_file = "/root/sovereign/backend/main.py"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Force patching main.py via SFTP...")
        
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        
        print("Patch uploaded. Verifying content on server...")
        stdin, stdout, stderr = ssh.exec_command(f"grep -n 'watchdog =' {remote_file}")
        print(f"Server content check:\n{stdout.read().decode()}")
        
        print("Restarting engine...")
        launch = "pkill -f uvicorn || true; cd /root/sovereign/backend && nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &"
        ssh.exec_command(launch)
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_patch()

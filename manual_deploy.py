import paramiko
import time

def deploy():
    # Credentials
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {host}...")
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Cleaning up and setting up directories...")
        
        # Cleanup and Setup
        cmds = [
            "rm -rf sovereign sovereign_old code.zip src_backup",
            "mkdir -p sovereign",
            "ufw disable"
        ]
        for c in cmds:
            ssh.exec_command(c)
            time.sleep(1)
            
        print("Uploading source zip...")
        sftp = ssh.open_sftp()
        sftp.put("sovereign_v15_light.zip", "/root/code.zip")
        sftp.close()
        
        print("Extracting and installing...")
        final_cmds = [
            "unzip -o /root/code.zip -d /root/sovereign/",
            "cd /root/sovereign/backend && pip3 install -r requirements.txt --break-system-packages",
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 5000 --break-system-packages > backend.log 2>&1 &"
        ]
        
        for c in final_cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Exit status: {exit_status}")
            
        print("DEPLOYMENT SUCCESSFUL! BACKEND IS LIVE.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deploy()

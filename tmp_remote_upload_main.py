import paramiko
import os

def upload_main_py():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    local_path = "c:\\Users\\Admin\\23226\\backend\\main.py"
    remote_path = "/root/sovereign/backend/main.py"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        
        print(f"Uploaded {local_path} to {remote_path}")
        
        # Restart backend
        print("Restarting backend container...")
        ssh.exec_command("docker restart sovereign_v15_backend")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_main_py()

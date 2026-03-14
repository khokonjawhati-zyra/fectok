import paramiko
import os

def master_healing_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading Master Healing Patch ---")
        sftp.put(r"c:\Users\Admin\23226\backend\main.py", "/root/sovereign/backend/main.py")
        sftp.put(r"c:\Users\Admin\23226\sovereign_media_hub\processor\processor_engine.py", "/root/sovereign/sovereign_media_hub/processor/processor_engine.py")
        sftp.close()
        
        print("--- REBUILDING & RESTARTING SERVICES ---")
        # Build backend and processor
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build backend_node ai_processor && docker-compose up -d backend_node ai_processor")
        print(stdout.read().decode())
        
        print("--- HEALING COMPLETED ---")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    master_healing_patch()

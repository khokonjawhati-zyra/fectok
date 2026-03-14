import paramiko
import os

def apply_full_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading Updated Processor Files ---")
        sftp.put(r"c:\Users\Admin\23226\sovereign_media_hub\processor\processor_engine.py", "/root/sovereign/sovereign_media_hub/processor/processor_engine.py")
        sftp.put(r"c:\Users\Admin\23226\sovereign_media_hub\processor\Dockerfile", "/root/sovereign/sovereign_media_hub/processor/Dockerfile")
        sftp.close()
        
        print("--- Rebuilding and Restarting AI Processor (with Logs) ---")
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build ai_processor && docker-compose up -d ai_processor")
        print(stdout.read().decode())
        
        print("--- Waiting for Pulse (10s) ---")
        import time
        time.sleep(10)
        
        print("--- Verifying Logs ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_processor")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_full_fix()

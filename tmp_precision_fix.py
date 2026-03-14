import paramiko
import os

def apply_ffmpeg_precision_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading Precision Processor Engine ---")
        sftp.put(r"c:\Users\Admin\23226\sovereign_media_hub\processor\processor_engine.py", "/root/sovereign/sovereign_media_hub/processor/processor_engine.py")
        sftp.close()
        
        print("--- REBUILDING Processor (Precision Mode) ---")
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build ai_processor && docker-compose up -d ai_processor")
        print(stdout.read().decode())
        
        print("--- Purging existing shards to force precision re-sharding ---")
        ssh.exec_command("find /var/www/html/media/videos/ -maxdepth 1 -type d -not -path '/var/www/html/media/videos/' -exec rm -rf {} +")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_ffmpeg_precision_fix()

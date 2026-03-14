import paramiko
import os

def master_hard_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- FIX 1: Healing Linux Permissions (403 Forbidden Fix) ---")
        ssh.exec_command("chmod -R 755 /root/sovereign/")
        ssh.exec_command("chmod -R 755 /var/www/html/media/videos/")
        ssh.exec_command("chown -R root:root /var/www/html/media/videos/")
        
        print("--- FIX 2: Purging Old Ghost Processes & Clearing Cache ---")
        # Kill any stuck ffmpeg or old processor instances
        ssh.exec_command("pkill -9 ffmpeg")
        # Clean potential broken/old sharded folders to force fresh ABR
        # Note: We only delete directories, keeping original mp4s
        ssh.exec_command("find /var/www/html/media/videos/ -maxdepth 1 -type d -not -path '/var/www/html/media/videos/' -exec rm -rf {} +")
        
        print("--- FIX 3: Rebuilding V15 Ecosystem (Hard Pulse) ---")
        # Direct docker-compose reset
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build --no-cache && docker-compose up -d")
        print(stdout.read().decode())
        
        print("--- MASTER HARD FIX COMPLETED ---")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    master_hard_fix()

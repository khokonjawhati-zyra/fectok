import paramiko
import os

def verify_master():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        target_file = "/var/www/html/media/videos/grok_video_2026-02-22-15-41-20_1773324895/index.m3u8"
        
        print(f"--- Final Master Playlist Check ---")
        stdin, stdout, stderr = ssh.exec_command(f"cat {target_file}")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_master()

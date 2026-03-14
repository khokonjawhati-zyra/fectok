import paramiko
import os

def check_structure_pulse():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        target_dir = "/var/www/html/media/videos/grok_video_2026-02-22-15-41-20_1773324895"
        
        print(f"--- Checking Directory STRUCTURE Pulse: {target_dir} ---")
        stdin, stdout, stderr = ssh.exec_command(f"ls -R {target_dir}")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_structure_pulse()

import paramiko
import os

def check_hls_details():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        target_dir = "/var/www/html/media/videos/grok_video_2026-02-22-15-51-39_1773333314"
        
        print(f"--- Checking Directory: {target_dir} ---")
        stdin, stdout, stderr = ssh.exec_command(f"ls -R {target_dir}")
        print(stdout.read().decode())
        
        print("--- Checking index.m3u8 Content ---")
        stdin, stdout, stderr = ssh.exec_command(f"cat {target_dir}/index.m3u8")
        print(stdout.read().decode())
        
        print("--- Checking 360p/playlist.m3u8 Content ---")
        stdin, stdout, stderr = ssh.exec_command(f"cat {target_dir}/360p/playlist.m3u8 | head -n 10")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_hls_details()

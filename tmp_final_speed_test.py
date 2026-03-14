import paramiko
import os
import time

def final_speed_test():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        target = "/var/www/html/media/videos/grok_video_2026-02-22-15-06-12_1773314149/360p/playlist.m3u8"
        print(f"--- WAITING FOR PRECISION SHARD: {target} ---")
        
        for _ in range(10):
            stdin, stdout, stderr = ssh.exec_command(f"ls {target}")
            if stdout.read().decode().strip():
                print("Playlist found! Checking timing...")
                stdin, stdout, stderr = ssh.exec_command(f"cat {target} | grep EXTINF | head -n 5")
                print(stdout.read().decode())
                break
            time.sleep(5)
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_speed_test()

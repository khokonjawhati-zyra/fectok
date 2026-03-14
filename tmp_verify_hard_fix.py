import paramiko
import os

def check_after_hard_fix_safe():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- FINAL VERIFICATION: Fragment Time & Permissions ---")
        # 1. Check if containers are UP
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}}\t{{.Status}}'")
        print(f"Containers Status:\n{stdout.read().decode()}")
        
        # 2. Check if processing has started on new mp4s
        stdin, stdout, stderr = ssh.exec_command("ls -R /var/www/html/media/videos/ | grep index.m3u8 | head -n 5")
        print(f"New HLS Playlists:\n{stdout.read().decode()}")
        
        # 3. Check fragment timing of ANY playlist to see if it's now 2s
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -name playlist.m3u8 | head -n 1")
        new_playlist = stdout.read().decode().strip()
        if new_playlist:
            print(f"Inspecting Playlist: {new_playlist}")
            stdin, stdout, stderr = ssh.exec_command(f"cat {new_playlist} | grep EXTINF")
            print(stdout.read().decode())
        else:
            print("No playlists found yet.")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_after_hard_fix_safe()

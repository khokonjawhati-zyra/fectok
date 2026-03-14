import paramiko
import os

def check_fresh_shards():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Checking for RECENTLY created Playlists ---")
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -name playlist.m3u8 -mmin -2")
        files = stdout.read().decode().strip().split('\n')
        
        if files and files[0]:
            for f in files:
                print(f"Inspecting Fresh Playlist: {f}")
                stdin, stdout, stderr = ssh.exec_command(f"cat {f} | grep EXTINF | head -n 3")
                print(stdout.read().decode())
        else:
            print("No playlists created in the last 2 minutes.")
            
        print("--- Processor Log Check ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_processor --tail 30")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_fresh_shards()

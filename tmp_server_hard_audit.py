import paramiko
import os

def live_hard_audit():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- AUDIT 1: Video Fragment Duration Check ---")
        # Find a playlist and check the fragment sequence
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -name playlist.m3u8 | head -n 1")
        playlist = stdout.read().decode().strip()
        if playlist:
            print(f"Checking Playlist: {playlist}")
            stdin, stdout, stderr = ssh.exec_command(f"cat {playlist} | grep '#EXTINF'")
            print(stdout.read().decode())
        
        print("--- AUDIT 2: Nginx Real-time Response Header ---")
        # Check if Nginx serves with correct Cache and Range headers
        stdin, stdout, stderr = ssh.exec_command("curl -I -L http://localhost/stream/test_check.m3u8")
        print(stdout.read().decode())
        
        print("--- AUDIT 3: Process Health (CPU/RAM) ---")
        # Check if FFmpeg is overloading the CPU
        stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep -E 'ffmpeg|python|nginx' | head -n 5")
        print(stdout.read().decode())

        print("--- AUDIT 4: Persistence Verification ---")
        # Check if registry.json actually has hls_ready=True on disk
        stdin, stdout, stderr = ssh.exec_command("grep -c '\"hls_ready\": true' /var/lib/sovereign/auth/registry.json")
        count = stdout.read().decode().strip()
        print(f"HLS Ready Videos on Disk: {count}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    live_hard_audit()

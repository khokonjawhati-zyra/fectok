import paramiko
import os

def check_hls_bitrate():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- AUDIT: HLS Segment Bitrate Check ---")
        # Find a 360p segment and check its size/duration
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -name '*.ts' | grep '360p' | head -n 1")
        segment = stdout.read().decode().strip()
        
        if segment:
            print(f"Inspecting Segment: {segment}")
            stdin, stdout, stderr = ssh.exec_command(f"ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 {segment}")
            print(f"Bitrate: {stdout.read().decode().strip()} bps")
            
            # Check Nginx Logs for Latency
            print("\n--- Nginx Access Log (Last 5 HLS Requests) ---")
            stdin, stdout, stderr = ssh.exec_command("tail -n 50 /var/log/nginx/access.log | grep '.ts' | tail -n 5")
            print(stdout.read().decode())
        else:
            print("No segments found to audit.")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_hls_bitrate()

import paramiko
import os

def check_hls_structure():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Checking Media Garden Structure (/var/www/html/media/videos) ---")
        stdin, stdout, stderr = ssh.exec_command("ls -R /var/www/html/media/videos/ | head -n 50")
        output = stdout.read().decode()
        print(output)
        
        print("--- Checking for index.m3u8 files ---")
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -name index.m3u8 | head -n 10")
        print(stdout.read().decode())
        
        print("--- Checking internal directory of a video ---")
        # Find first directory
        stdin, stdout, stderr = ssh.exec_command("find /var/www/html/media/videos/ -maxdepth 1 -type d | tail -n 1")
        dir_path = stdout.read().decode().strip()
        if dir_path and dir_path != "/var/www/html/media/videos/":
            print(f"Checking directory: {dir_path}")
            stdin, stdout, stderr = ssh.exec_command(f"ls -R {dir_path}")
            print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_hls_structure()

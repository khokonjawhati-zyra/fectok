import os
import paramiko

def final_push():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    local_zip = "sovereign_v1.5.3_mirror.zip"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=30)
        print("CONNECTED. PREPARING SERVER...")
        
        # Ensure unzip and mkdir
        ssh.exec_command("apt-get update && apt-get install -y unzip")
        ssh.exec_command("mkdir -p /root/sovereign")
        
        print(f"UPLOADING {local_zip} (This may take a minute)...")
        sftp = ssh.open_sftp()
        sftp.put(local_zip, "/root/sovereign_sync.zip")
        sftp.close()
        
        print("EXTRACTING...")
        cmds = [
            "rm -rf /root/sovereign",
            "unzip -o /root/sovereign_sync.zip -d /root/",
            "mv /root/sovereign /root/sovereign_tmp && mv /root/sovereign_tmp/* /root/sovereign/ || true", # Fix nested zip structure if any
            "rm /root/sovereign_sync.zip",
            "cd /root/sovereign && python3 route_ui.py",
            "cd /root/sovereign && docker-compose down || true",
            "cd /root/sovereign && docker-compose up -d --build",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Server Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- V1.5.3 MIRROR SYNC IS NOW LIVE ---")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_push()

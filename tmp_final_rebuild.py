import paramiko
import os

def final_server_rebuild():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading ALL Core Server Files (V15 Master Sync) ---")
        sftp.put(r"c:\Users\Admin\23226\backend\main.py", "/root/sovereign/backend/main.py")
        sftp.put(r"c:\Users\Admin\23226\sovereign_media_hub\uplink\uplink_server.py", "/root/sovereign/sovereign_media_hub/uplink/uplink_server.py")
        sftp.close()
        
        print("--- REBUILDING ECOSYSTEM (Backend + Uplink) ---")
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build backend_node uplink_hub && docker-compose up -d backend_node uplink_hub")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- ECOSYSTEM PULSE STARTED ---")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_server_rebuild()

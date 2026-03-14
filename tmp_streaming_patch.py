import paramiko
import os

def final_streaming_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading Final Streaming Patch ---")
        sftp.put(r"c:\Users\Admin\23226\nginx.conf", "/root/sovereign/nginx.conf")
        sftp.put(r"c:\Users\Admin\23226\backend\main.py", "/root/sovereign/backend/main.py")
        sftp.close()
        
        print("--- Rebuilding Backend & Reloading Nginx ---")
        # Build backend to apply PROXY_PATH change
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build backend_node && docker-compose up -d backend_node")
        print(stdout.read().decode())
        
        # Restart Nginx container to apply new /stream/ location
        stdin, stdout, stderr = ssh.exec_command("docker restart sovereign_v15_gateway")
        print("Nginx Gateway Restarted.")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_streaming_patch()

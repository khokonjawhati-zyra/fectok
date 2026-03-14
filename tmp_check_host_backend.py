import paramiko
import os

def check_host_backend():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Host Backend main.py Check ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/backend/main.py | grep -n '/api/v15/media/hls_ready'")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_host_backend()

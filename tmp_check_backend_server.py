import paramiko
import os

def check_backend_logs():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Backend Container Status ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep backend")
        print(stdout.read().decode())
        
        print("--- Backend Logs (Filter for hls_ready) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend | grep hls_ready")
        print(stdout.read().decode())
        
        print("--- Backend main.py Check ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend cat /app/main.py | grep -n '/api/v15/media/hls_ready'")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_backend_logs()

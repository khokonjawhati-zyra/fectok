import paramiko
import os

def check_connectivity():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Checking Network Ports (80 & 443) ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tuln | grep -E ':80|:443'")
        print(stdout.read().decode())
        
        print("--- Checking Docker Container Logs (Gateway) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_gateway --tail 20")
        print(stdout.read().decode())
        
        print("--- Checking Docker Container Status ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_connectivity()

import paramiko
import os

def check_processor_properly():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Docker Status (Real) ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}}\t{{.Status}}'")
        print(stdout.read().decode())
        
        print("--- Processor Internal Log File ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_processor cat /app/processor.log | tail -n 50")
        print(stdout.read().decode())
        
        print("--- Processor Working Dir Check ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_processor ls -la /app/")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_processor_properly()

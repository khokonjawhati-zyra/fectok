import paramiko
import os

def check_docker_status():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Docker ps ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps -a")
        print(stdout.read().decode())
        
        print("--- Processor Error Logs (File) ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/sovereign_media_hub/processor/processor_error.log | tail -n 20")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_docker_status()

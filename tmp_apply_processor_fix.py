import paramiko
import os

def check_host_code():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Host Processor Engine Code Check ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/sovereign_media_hub/processor/processor_engine.py | grep -A 5 'qualities ='")
        print(stdout.read().decode())
        
        print("--- Rebuilding and Restarting AI Processor ---")
        stdin, stdout, stderr = ssh.exec_command("cd /root/sovereign && docker-compose build ai_processor && docker-compose up -d ai_processor")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_host_code()

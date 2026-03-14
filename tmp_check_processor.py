import paramiko
import os

def check_processor_logs():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Processor Container Logs (last 50 lines) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_processor --tail 50")
        print(stdout.read().decode())
        
        print("--- Processor Engine File Check ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/sovereign_media_hub/processor/processor_engine.py | grep -A 20 'qualities ='")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_processor_logs()

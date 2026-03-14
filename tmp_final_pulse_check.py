import paramiko
import os

def final_pulse_check():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- FINAL LOGS: Processor (Notification Check) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_processor | tail -n 20")
        print(stdout.read().decode())
        
        print("--- FINAL LOGS: Backend (Endpoint Pulse Check) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend | grep hls_ready | tail -n 5")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_pulse_check()

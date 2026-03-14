import paramiko
import sys

def diagnose_remote():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- RUNNING CONTAINERS ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        print(stdout.read().decode())
        
        print("--- LISTENING PORTS ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tulnp")
        print(stdout.read().decode())
        
        print("--- BACKEND LOGS (Last 20 lines) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend --tail 20")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose_remote()

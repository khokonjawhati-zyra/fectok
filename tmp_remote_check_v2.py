import paramiko

def diagnose_remote():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- CONTAINER LIST ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}} - {{.Status}}'")
        print(stdout.read().decode())
        
        print("--- APP PORT 5000 CHECK ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep :5000")
        print(stdout.read().decode())
        
        print("--- BACKEND LOG ERRORS (Last 10 lines) ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend 2>&1 | tail -n 10")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose_remote()

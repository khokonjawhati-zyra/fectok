import paramiko

def debug_remote():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Status of Backend Process ---")
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep uvicorn")
        print(stdout.read().decode())
        
        print("--- Last 20 lines of backend.log ---")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /root/sovereign/backend/backend.log")
        print(stdout.read().decode())
        
        print("--- Network Listen Status ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep 5000")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_remote()

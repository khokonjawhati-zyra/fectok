import paramiko

def debug_paths():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Root Listing ---")
        stdin, stdout, stderr = ssh.exec_command("ls -F /root/")
        print(stdout.read().decode())
        
        print("--- Sovereign Listing ---")
        stdin, stdout, stderr = ssh.exec_command("ls -F /root/sovereign/")
        print(stdout.read().decode())
        
        print("--- Sovereign Backend Listing ---")
        stdin, stdout, stderr = ssh.exec_command("ls -F /root/sovereign/backend/")
        print(stdout.read().decode())
        
        print("--- Current Directory ---")
        stdin, stdout, stderr = ssh.exec_command("pwd")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_paths()

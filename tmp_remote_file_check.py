import paramiko

def check_remote_files():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- CHECKING FOR imperial_finance.py ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend ls /app/imperial_finance.py")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("--- CHECKING FOR SYNTAX ERRORS ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend python -m py_compile /app/imperial_finance.py")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_files()

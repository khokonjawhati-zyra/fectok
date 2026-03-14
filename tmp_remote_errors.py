import paramiko

def check_remote_errors():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- SEARCHING FOR EXCEPTIONS IN BACKEND LOGS ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend 2>&1 | grep -i 'Traceback\|Error' | tail -n 20")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_errors()

import paramiko

def check_docker_v3():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Docker PS (All) ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps -a")
        # Use errors='ignore' in decode to avoid codec issues
        print(stdout.read().decode('utf-8', 'ignore'))
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_docker_v3()

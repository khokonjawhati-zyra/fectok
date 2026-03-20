import paramiko

def get_docker_compose():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Searching for docker-compose.yml...")
        stdin, stdout, stderr = ssh.exec_command("find / -name docker-compose.yml 2>/dev/null | head -n 1")
        path = stdout.read().decode().strip()
        
        if path:
            print(f"Found docker-compose.yml at {path}")
            stdin, stdout, stderr = ssh.exec_command(f"cat {path}")
            print(stdout.read().decode())
        else:
            print("docker-compose.yml not found.")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_docker_compose()

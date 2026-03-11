import paramiko

def check_docker_v2():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Docker PS (All) ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps -a")
        print(stdout.read().decode())
        
        print("--- Docker Compose Content ---")
        stdin, stdout, stderr = ssh.exec_command("cat /root/sovereign/docker-compose.yml")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_docker_v2()

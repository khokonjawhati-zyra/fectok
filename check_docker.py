import paramiko

def check_docker_health():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Docker Container Status (Live) ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'")
        print(stdout.read().decode())
        
        print("--- Checking for Docker Engine (Daemon) ---")
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active docker")
        print(f"Docker Daemon: {stdout.read().decode().strip()}")
        
        print("--- Checking Project Directory ---")
        stdin, stdout, stderr = ssh.exec_command("ls -F /root/sovereign/")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_docker_health()

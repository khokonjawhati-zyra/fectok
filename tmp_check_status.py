import paramiko

def check_remote_status():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=pw, timeout=30)
        
        print("--- DOCKER CONTAINERS ---")
        stdin, stdout, stderr = ssh.exec_command('docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"')
        print(stdout.read().decode())
        
        print("\n--- ERROR LOGS (LAST 20 LINES) ---")
        stdin, stdout, stderr = ssh.exec_command('docker-compose logs --tail 20')
        print(stdout.read().decode())
        
        print("\n--- PORT CHECK (80/443) ---")
        stdin, stdout, stderr = ssh.exec_command('netstat -tpln | grep -E ":80|:443"')
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"FAILED TO CONNECT: {e}")

if __name__ == "__main__":
    check_remote_status()

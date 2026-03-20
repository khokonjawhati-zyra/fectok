import paramiko

def check_server_status():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected to server.")
        
        commands = [
            "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'",
            "ps aux | grep uvicorn",
            "netstat -tupln | grep 5000",
            "tail -n 20 /root/sovereign/backend/backend.log"
        ]
        
        for cmd in commands:
            print(f"\n--- Result of: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_server_status()

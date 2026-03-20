import paramiko

def diagnose_live_server():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- Nginx Status ---")
        stdin, stdout, stderr = ssh.exec_command("systemctl status nginx")
        print(stdout.read().decode())
        
        print("--- Docker Status ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps -a")
        print(stdout.read().decode())
        
        print("--- Port 80/443 Listen Status ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tulnp | grep -E ':80|:443'")
        print(stdout.read().decode())

        print("--- Firewall (UFW) Status ---")
        stdin, stdout, stderr = ssh.exec_command("ufw status")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    diagnose_live_server()

import paramiko

def check_domain():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Web Server Ports (80/443) ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep -E ':80|:443'")
        print(stdout.read().decode())
        
        print("--- Nginx Status ---")
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active nginx || echo 'nginx not installed/active'")
        print(stdout.read().decode())
        
        print("--- Nginx Configs ---")
        stdin, stdout, stderr = ssh.exec_command("ls /etc/nginx/sites-enabled/ || echo 'no nginx sites'")
        print(stdout.read().decode())
        
        print("--- Let's Encrypt Certificates ---")
        stdin, stdout, stderr = ssh.exec_command("ls /etc/letsencrypt/live/ || echo 'no certificates found'")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_domain()

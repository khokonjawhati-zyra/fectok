import paramiko

def start_remote_nginx():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Starting Nginx on remote server...")
        stdin, stdout, stderr = ssh.exec_command("systemctl start nginx")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("Checking status again...")
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active nginx")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_remote_nginx()

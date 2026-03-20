import paramiko

def read_nginx_properly():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Read the whole file
        cmd = "cat /etc/nginx/sites-enabled/sovereign"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        content = stdout.read().decode('utf-8')
        
        print("--- NGINX CONFIG START ---")
        print(content)
        print("--- NGINX CONFIG END ---")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_nginx_properly()

import paramiko

def download_nginx_config():
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
        
        with open("sovereign_nginx.conf", "w") as f:
            f.write(content)
        
        print("Successfully downloaded nginx config to local file: sovereign_nginx.conf")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_nginx_config()

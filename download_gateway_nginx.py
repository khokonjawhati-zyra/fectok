import paramiko

def download_file(remote, local):
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        stdin, stdout, stderr = ssh.exec_command(f"cat {remote}")
        content = stdout.read().decode()
        
        with open(local, "w") as f:
            f.write(content)
        
        print(f"Downloaded {remote} to {local}")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_file("/root/sovereign/nginx.conf", "remote_nginx_container.conf")

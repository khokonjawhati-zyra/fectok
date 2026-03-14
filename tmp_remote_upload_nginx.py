import paramiko
import os

def upload_nginx_conf():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    local_path = "c:\\Users\\Admin\\23226\\nginx.conf"
    remote_path = "/root/sovereign/nginx.conf"
    
    with open(local_path, 'r') as f:
        content = f.read()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Use SFTP or just echo to write the file
        sftp = ssh.open_sftp()
        with sftp.file(remote_path, 'w') as f:
            f.write(content)
        sftp.close()
        
        print(f"Uploaded {local_path} to {remote_path}")
        
        # Reload nginx in container
        print("Reloading Nginx in gateway container...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway nginx -s reload")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_nginx_conf()

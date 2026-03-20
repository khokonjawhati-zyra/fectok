import paramiko

def check_nginx_upload_config():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Checking for /stream location in Nginx config...")
        cmd = "grep -r '/stream' /etc/nginx/sites-enabled/"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        
        print("Checking for /video_stream location...")
        cmd = "grep -r '/video_stream' /etc/nginx/sites-enabled/"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nginx_upload_config()

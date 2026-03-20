import paramiko

def debug_nginx_failure():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Checking nginx configuration syntax...")
        stdin, stdout, stderr = ssh.exec_command("nginx -t")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("Checking recent nginx error logs...")
        stdin, stdout, stderr = ssh.exec_command("tail -n 20 /var/log/nginx/error.log")
        print(stdout.read().decode())
        
        print("Checking port 80 usage...")
        stdin, stdout, stderr = ssh.exec_command("netstat -tulnp | grep :80")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_nginx_failure()

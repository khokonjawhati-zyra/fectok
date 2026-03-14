import paramiko

def check_nginx_stats():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- nginx.conf stats on remote ---")
        stdin, stdout, stderr = ssh.exec_command("ls -l /root/sovereign/nginx.conf")
        print(stdout.read().decode())
        
        print("--- checking for syntax errors in nginx ---")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway nginx -t")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nginx_stats()

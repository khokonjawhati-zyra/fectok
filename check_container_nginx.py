import paramiko

def check_container_nginx():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Reading nginx config inside sovereign_v15_gateway...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway cat /etc/nginx/nginx.conf")
        print(stdout.read().decode())
        
        print("Checking for conf.d files...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway ls /etc/nginx/conf.d")
        print(stdout.read().decode())

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_container_nginx()

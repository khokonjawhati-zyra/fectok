import paramiko

def check_nginx():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- NGINX ACCESS LOG (Last 5 lines) ---")
        # Find where nginx logs are. In docker it might be stdout.
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_gateway --tail 10")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nginx()

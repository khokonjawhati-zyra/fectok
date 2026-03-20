import paramiko

def check_gateway_443():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Checking for 'listen 443' inside gateway container...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway grep -r 'listen 443' /etc/nginx/")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_gateway_443()

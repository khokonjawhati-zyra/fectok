import paramiko

def diagnose_server_fully():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Checking all running containers...")
        stdin, stdout, stderr = ssh.exec_command("docker ps")
        print(stdout.read().decode())
        
        print("Testing localhost curl...")
        stdin, stdout, stderr = ssh.exec_command("curl -I http://localhost")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        print("Checking fectok.com nginx config INSIDE the gateway container...")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_gateway cat /etc/nginx/conf.d/default.conf")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose_server_fully()

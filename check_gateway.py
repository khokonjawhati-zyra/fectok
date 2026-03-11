import paramiko

def check_gateway():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Gateway Logs ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_gateway")
        print(stdout.read().decode('utf-8', 'ignore'))
        print(stderr.read().decode('utf-8', 'ignore'))
        
        print("--- Port 80 Check ---")
        stdin, stdout, stderr = ssh.exec_command("netstat -tupln | grep :80")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_gateway()

import paramiko

def check_docker_logs():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Backend Logs ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_backend")
        print(stdout.read().decode('utf-8', 'ignore'))
        print(stderr.read().decode('utf-8', 'ignore'))
        
        print("--- Uplink Logs ---")
        stdin, stdout, stderr = ssh.exec_command("docker logs sovereign_v15_uplink")
        print(stdout.read().decode('utf-8', 'ignore'))
        print(stderr.read().decode('utf-8', 'ignore'))
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_docker_logs()

import paramiko

def verify_infra():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("VERIFYING DOCKER INFRA...")
        
        cmds = [
            "docker --version",
            "docker compose version",
            "ls -la /root"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print("STDOUT:", stdout.read().decode())
            print("STDERR:", stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error checking infra: {e}")

if __name__ == "__main__":
    verify_infra()

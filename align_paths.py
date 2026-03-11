import paramiko

def align_paths():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("ALIDNING PATHS...")
        
        cmds = [
            "ls -F /root/sovereign", # Look for nested sovereign
            "mv /root/sovereign/sovereign/* /root/sovereign/ || echo 'No nested folder'",
            "ls -F /root/sovereign",
            "cd /root/sovereign && docker-compose build", # Rebuild with correct paths
            "cd /root/sovereign && docker-compose up -d",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Execute: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    align_paths()

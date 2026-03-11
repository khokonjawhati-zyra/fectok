import paramiko

def normalize_and_restart():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("NORMALIZING FILE STRUCTURE...")
        
        cmds = [
            "mv /root/sovereign/sovereign/* /root/sovereign/ || true",
            "mv /root/sovereign/sovereign/.* /root/sovereign/ || true",
            "rm -rf /root/sovereign/sovereign",
            "ls -F /root/sovereign",
            "cd /root/sovereign && docker-compose down",
            "cd /root/sovereign && docker-compose up -d --build",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- NORMALIZATION COMPLETE ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    normalize_and_restart()

import paramiko

def surgical_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=30)
        print("PERFORMING SURGICAL FIX ON DOCKER CONFIGS...")
        
        # 1. Upload the FIXED docker-compose.yml
        sftp = ssh.open_sftp()
        sftp.put("docker-compose.yml", "/root/sovereign/docker-compose.yml")
        sftp.close()
        
        # 2. Restart with rebuild to ensure fresh state inside containers
        print("Re-igniting Ecosystem with fixed mounts...")
        cmds = [
            "cd /root/sovereign && docker compose down && docker compose up -d --build",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode(errors='ignore'))
            print(stderr.read().decode(errors='ignore'))
            
        ssh.close()
        print("--- SURGICAL FIX COMPLETE ---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    surgical_fix()

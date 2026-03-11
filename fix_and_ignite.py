import paramiko

def fix_and_ignite():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("CONNECTED. RESTRUCTURING SERVER PATHS...")
        
        cmds = [
            # 1. Rename the folder back to sovereign
            "mv /root/sovereign_tmp /root/sovereign",
            "ls -ld /root/sovereign",
            
            # 2. Re-run route setup to confirm everything is in place
            "cd /root/sovereign && python3 route_ui.py",
            
            # 3. Final Docker Ignition
            "cd /root/sovereign && docker-compose down",
            "cd /root/sovereign && docker-compose up -d --build",
            
            # 4. Status Check
            "docker ps",
            "docker network ls"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- SOVEREIGN IS OFFICIALLY REBORN IN V1.5.3 ---")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    fix_and_ignite()

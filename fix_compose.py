import paramiko

def fix_compose():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Fixing docker-compose.yml paths...")
        
        # Replace /opt/sovereign/core/ with /root/sovereign/
        # Also fix specific sub-paths if needed.
        # backend -> ./backend
        # uplink -> ./sovereign_media_hub/uplink
        
        cmds = [
            # 1. Backup
            "cp /root/sovereign/docker-compose.yml /root/sovereign/docker-compose.yml.bak",
            # 2. Patching Backend Volume
            "sed -i 's|/opt/sovereign/core/backend|./backend|g' /root/sovereign/docker-compose.yml",
            # 3. Patching Uplink Volume
            "sed -i 's|/opt/sovereign/core/uplink|./sovereign_media_hub/uplink|g' /root/sovereign/docker-compose.yml",
            # 4. Check results
            "cat /root/sovereign/docker-compose.yml | grep -A 5 'volumes:'",
            # 5. Restart
            "cd /root/sovereign && docker-compose down && docker-compose up -d",
            "sleep 10",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            print(stdout.read().decode('utf-8', 'ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_compose()

import paramiko

def remote_ignite():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    try:
        print(f"Connecting to Sovereign Live Node: {host} for Surgical Patch Ignition...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=pw, timeout=30)
        
        # Commands to update and restart
        commands = [
            "cd /root/sovereign",
            "git pull origin main",
            "docker-compose down",
            "docker-compose up -d --build",
            "docker ps"
        ]
        
        full_command = " && ".join(commands)
        stdin, stdout, stderr = ssh.exec_command(full_command)
        
        print("\n--- DEPLOYMENT LOGS ---")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
        print("\nIGNITION COMPLETE! V15-SSL-PATCH ACTIVE.")
        return True
    except Exception as e:
        print(f"IGNITION FAILED: {e}")
        return False

if __name__ == "__main__":
    remote_ignite()

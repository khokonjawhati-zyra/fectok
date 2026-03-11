import paramiko

def fix_gateway():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("FIXING GATEWAY AND KILLING ROGUE NGINX...")
        
        cmds = [
            # 1. Kill any process on port 80/443
            "fuser -k 80/tcp || true",
            "fuser -k 443/tcp || true",
            "pkill -9 nginx || true",
            # 2. Restart Native Nginx (since that was working earlier)
            "systemctl start nginx",
            "systemctl status nginx | grep Active",
            # 3. Double check port 80
            "netstat -tupln | grep :80"
        ]
        
        for c in cmds:
            print(f"\nExecuting: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            print(stdout.read().decode('utf-8', 'ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_gateway()

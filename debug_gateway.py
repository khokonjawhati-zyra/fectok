import paramiko

def debug_gateway():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("DEBUGGING GATEWAY...")
        
        cmds = [
            "docker logs sovereign_v15_gateway",
            "ls -la /root/sovereign/user_panel/build/web",
            "ls -la /root/sovereign/admin_panel/build/web",
            "cat /root/sovereign/nginx.conf"
        ]
        
        for c in cmds:
            print(f"--- RUNNING: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Use small delay for logs
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_gateway()

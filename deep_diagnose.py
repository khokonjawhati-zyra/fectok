import paramiko

def deep_diagnose():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("DIAGNOSING CRITICAL FAILURES...")
        
        cmds = [
            # Check structure
            "ls -la /root/sovereign",
            "ls -la /root/sovereign/webadmin_panel",
            
            # Backend Logs
            "docker logs sovereign_v15_backend",
            
            # Uplink Logs
            "docker logs sovereign_v15_uplink",
            
            # Config Check
            "cat /root/sovereign/nginx.conf"
        ]
        
        for c in cmds:
            print(f"--- {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode(errors='ignore'))
            print(stderr.read().decode(errors='ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deep_diagnose()

import paramiko

def diagnose():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("DIAGNOSING SERVER STATE...")
        
        cmds = [
            "ls -ld /root/sovereign",
            "ls -ld /root/sovereign_tmp",
            "ls -R /root | head -n 20",
            "ls /root/sovereign/sovereign" # Check for nested folders
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose()

import paramiko

def check_status():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("VERIFYING LIVE DEPLOYMENT...")
        
        cmds = [
            "docker ps",
            "curl -sI -H 'Host: vazo.fectok.com' localhost",
            "docker logs sovereign_v15_gateway --tail 5"
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
    check_status()

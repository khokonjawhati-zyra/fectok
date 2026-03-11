import paramiko

def verify_all():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("FINAL VERIFICATION...")
        
        cmds = [
            "docker ps -a",
            "curl -sI -H 'Host: fectok.com' localhost",
            "curl -sI -H 'Host: vazo.fectok.com' localhost",
            "docker logs sovereign_v15_backend --tail 10",
            "docker logs sovereign_v15_gateway --tail 10"
        ]
        
        for c in cmds:
            print(f"--- {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_all()

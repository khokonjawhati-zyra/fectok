import paramiko

def fetch_logs():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("FETCHING ERROR LOGS...")
        
        cmds = [
            "docker logs sovereign_v15_backend --tail 50",
            "docker logs sovereign_v15_uplink --tail 50"
        ]
        
        for c in cmds:
            print(f"--- LOGS FOR: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_logs()

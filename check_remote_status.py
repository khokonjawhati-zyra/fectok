import paramiko

def check_status():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        
        commands = [
            "docker logs --tail 50 sovereign_v15_backend",
            "docker logs --tail 50 sovereign_v15_gateway",
            "docker logs --tail 50 sovereign_v15_uplink"
        ]
        
        for cmd in commands:
            print(f"--- EXECUTING: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_status()

import paramiko

def check_uplink_internal():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        cmd = "docker exec sovereign_v15_uplink ls -lh /app/vault/data | head -n 20"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("--- UPLINK INTERNAL LIST ---")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_uplink_internal()

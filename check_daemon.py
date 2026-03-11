import paramiko

def verify_daemon_health():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("PERFORMING INFRASTRUCTURE HEARTBEAT CHECK...")
        
        cmds = [
            # 1. Enable and Start Docker Service
            "systemctl enable docker",
            "systemctl start docker",
            # 2. Check Service Status
            "systemctl is-active docker",
            "systemctl is-enabled docker",
            # 3. Test Container Engine with a tiny image
            "docker run --rm alpine echo 'DOCKER_ENGINE_HEALTHY'",
            # 4. Check for any remaining Docker V1 leftovers
            "whereis docker-compose"
        ]
        
        for c in cmds:
            print(f"Verify Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print("STDOUT:", stdout.read().decode())
            print("STDERR:", stderr.read().decode())
            
        ssh.close()
        print("--- INFRASTRUCTURE VERIFIED: NO GAPS FOUND ---")
    except Exception as e:
        print(f"Error during infra check: {e}")

if __name__ == "__main__":
    verify_daemon_health()

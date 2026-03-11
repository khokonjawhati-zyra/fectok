import paramiko

def build_docker_infra():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=60)
        print("CONNECTED. REBUILDING DOCKER INFRASTRUCTURE...")
        
        cmds = [
            # 1. Update and install base tools
            "apt-get update",
            "apt-get install -y ca-certificates curl gnupg unzip",
            
            # 2. Setup Docker Repository
            "install -m 0755 -d /etc/apt/keyrings",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes",
            "chmod a+r /etc/apt/keyrings/docker.gpg",
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null',
            
            # 3. Install Docker Engine & Compose V2
            "apt-get update",
            "apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
            
            # 4. Verify
            "docker --version",
            "docker compose version"
        ]
        
        for c in cmds:
            print(f"Build Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("--- INFRASTRUCTURE REBUILD COMPLETE: DOCKER V2 IS LIVE ---")
    except Exception as e:
        print(f"Error rebuilding infra: {e}")

if __name__ == "__main__":
    build_docker_infra()

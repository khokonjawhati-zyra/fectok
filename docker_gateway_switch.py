import paramiko

def docker_gateway_switch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Switching to Docker Gateway...")
        
        cmds = [
            # 1. Stop native nginx
            "systemctl stop nginx || true",
            "systemctl disable nginx || true",
            # 2. Start Docker gateway
            "cd /root/sovereign && docker-compose up -d stream_gateway",
            "sleep 5",
            # 3. Final Check
            "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            print(stdout.read().decode('utf-8', 'ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    docker_gateway_switch()

import paramiko

def kill_port_conflicts():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("CHECKING FOR PORT CONFLICTS...")
        
        cmds = [
            "netstat -tulpn | grep :80",
            "netstat -tulpn | grep :443",
            "fuser -k 80/tcp || true",
            "fuser -k 443/tcp || true",
            "service nginx stop || true",
            "service apache2 stop || true",
            "cd /root/sovereign && docker-compose restart stream_gateway",
            "sleep 5",
            "docker ps",
            "docker logs sovereign_v15_gateway"
        ]
        
        for c in cmds:
            print(f"--- EXEC: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_port_conflicts()

import paramiko
import time

def docker_absolute_ignition():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Stopping manual processes and igniting Docker...")
        
        # Killing manual backend explicitly
        cmds = [
            "pkill -f uvicorn || true",
            "cd /root/sovereign && docker-compose down",
            "cd /root/sovereign && docker-compose up -d",
            "sleep 10",
            "docker ps -a"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            # print(stdout.read().decode('utf-8', 'ignore')) # avoid codec issues
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    docker_absolute_ignition()

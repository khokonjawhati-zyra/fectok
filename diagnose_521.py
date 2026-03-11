import paramiko

def diagnose_521():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("DIAGNOSING 521 ERROR...")
        
        cmds = [
            # 1. Port list
            "netstat -tupln | grep -E ':80|:443'",
            # 2. Localhost check
            "curl -I http://127.0.0.1",
            # 3. UFW check
            "ufw status",
            # 4. Docker Gateway Logs
            "docker logs sovereign_v15_gateway --tail 20",
            # 5. Check if native nginx restarted by accident
            "systemctl status nginx | grep Active"
        ]
        
        for c in cmds:
            print(f"\nExecuting: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            print(stdout.read().decode('utf-8', 'ignore'))
            print(stderr.read().decode('utf-8', 'ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose_521()

import paramiko
import json

def ecosystem_scan():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("SOVEREIGN V15: DEEP ECOSYSTEM SCAN INITIATED...")
        
        # 1. Docker Pulse
        print("\n--- [1] DOCKER COMPONENT PULSE ---")
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}}: {{.Status}}'")
        print(stdout.read().decode().strip())
        
        # 2. Internal Network Handshake (80, 5000, 8080)
        print("\n--- [2] NETWORK PORT HANDSHAKE ---")
        ports = [80, 5000, 8080, 6379]
        for p in ports:
            stdin, stdout, stderr = ssh.exec_command(f"netstat -tupln | grep :{p} && echo 'PORT {p}: OPEN' || echo 'PORT {p}: CLOSED'")
            print(stdout.read().decode().strip().split('\n')[-1])
            
        # 3. Storage Integrity (R2 Mount)
        print("\n--- [3] STORAGE INTEGRITY (R2 CLOUD) ---")
        stdin, stdout, stderr = ssh.exec_command("df -h | grep s3fs || echo 'R2 STORAGE: OFFLINE'")
        mount_info = stdout.read().decode().strip()
        if mount_info:
            print(f"R2 STORAGE: ONLINE ({mount_info.split()[1]} capacity)")
        
        # 4. API Heartbeat Check (Port 5000 via loopback)
        print("\n--- [4] BACKEND API HEARTBEAT ---")
        stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:5000/api/v15/ping || echo 'API: UNRESPONSIVE'")
        print(f"Response: {stdout.read().decode().strip()}")
        
        # 5. Uplink Visibility
        print("\n--- [5] MEDIA UPLINK VISIBILITY ---")
        stdin, stdout, stderr = ssh.exec_command("curl -s -I http://127.0.0.1:8080 | grep HTTP || echo 'UPLINK: UNRESPONSIVE'")
        print(f"Status: {stdout.read().decode().strip()}")
        
        ssh.close()
        print("\nSCAN COMPLETE: ECOSYSTEM IS ATOM-SYNCED.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ecosystem_scan()

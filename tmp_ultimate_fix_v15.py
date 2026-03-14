import paramiko
import os

def ultimate_fix():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    sftp = ssh.open_sftp()
    
    # 1. Upload everything
    print("Uploading V15 Ecosystem Re-build Pack...")
    sftp.put(r'c:\Users\Admin\23226\backend\main.py', '/root/sovereign/backend/main.py')
    sftp.put(r'c:\Users\Admin\23226\backend\ai_engine.py', '/root/sovereign/backend/ai_engine.py')
    sftp.put(r'c:\Users\Admin\23226\nginx.conf', '/root/sovereign/nginx.conf')
    sftp.put(r'c:\Users\Admin\23226\tmp_dna_healing.py', '/root/sovereign/tmp_dna_healing.py')
    
    # 2. Execute DNA Healing (Persistent DBs)
    print("Executing DNA Healing on persistent databases...")
    stdin, stdout, stderr = ssh.exec_command('python3 /root/sovereign/tmp_dna_healing.py')
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # 3. Full Mesh Ignition
    print("Re-igniting Gateway & Backend Mesh...")
    # --force-recreate to ensure Nginx picks up the new config and resolver
    stdin, stdout, stderr = ssh.exec_command('cd /root/sovereign && docker-compose up -d --build --force-recreate stream_gateway backend_node')
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # 4. Final Pulse Verification
    print("Verifying Master Feed Pulse...")
    import time
    time.sleep(10)
    stdin, stdout, stderr = ssh.exec_command('curl -s https://fectok.com/api/v15/feed/foryou')
    response = stdout.read().decode()
    if 'SUCCESS' in response and 'https' in response:
        print("MASTER PULSE: OPERATIONAL. DNA Healed & SSL Locked.")
    else:
        print(f"MASTER PULSE: CAUTION. Response: {response[:200]}...")
    
    sftp.close()
    ssh.close()
    print("ULTIMATE V15 FIX COMPLETE.")

if __name__ == "__main__":
    ultimate_fix()

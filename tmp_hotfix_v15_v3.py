import paramiko
import os

def hotfix_v15():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    sftp = ssh.open_sftp()
    
    # 1. Upload fixed backend files
    print("Uploading fixed V15 Backend [main.py, ai_engine.py]...")
    sftp.put(r'c:\Users\Admin\23226\backend\main.py', '/root/sovereign/backend/main.py')
    sftp.put(r'c:\Users\Admin\23226\backend\ai_engine.py', '/root/sovereign/backend/ai_engine.py')
    
    # 2. Sync files to persistent storage (just in case)
    print("Syncing databases to persistent vault...")
    ssh.exec_command('mkdir -p /var/lib/sovereign/auth')
    ssh.exec_command('cp /root/sovereign/backend/*.json /var/lib/sovereign/auth/')
    
    # 3. Restart Backend Container
    print("Restarting V15 Backend Cluster...")
    # Using up -d --build to ensure all changes are reflected
    stdin, stdout, stderr = ssh.exec_command('cd /root/sovereign && docker-compose up -d --build backend_node')
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # 4. Verification Check
    print("Verifying Feed API Pulse...")
    import time
    time.sleep(5)
    stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5000/api/v15/feed/foryou')
    response = stdout.read().decode()
    if 'SUCCESS' in response:
        print("FEED PULSE: SUCCESS! Affinity Scorer Online.")
    else:
        print(f"FEED PULSE: FAILED. Response: {response}")
    
    sftp.close()
    ssh.close()
    print("HOTFIX DEPLOYMENT COMPLETE.")

if __name__ == "__main__":
    hotfix_v15()

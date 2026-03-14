import paramiko
import os
from scp import SCPClient

def deploy_heavy_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    scp = SCPClient(ssh.get_transport())
    
    # 1. Upload Backend Fix
    print("Uploading Backend Fix...")
    scp.put(r'c:\Users\Admin\23226\backend\main.py', '/root/sovereign/backend/main.py')
    
    # 2. Upload Nginx Config (just in case)
    print("Uploading Nginx Config...")
    scp.put(r'c:\Users\Admin\23226\nginx.conf', '/root/sovereign/nginx.conf')
    
    # 3. Upload Sound Engine (Recursive)
    print("Uploading Sound Engine...")
    ssh.exec_command('mkdir -p /root/sovereign/Sovereign_Sound_Loop')
    # scp.put doesn't do recursive directories easily without an extra step or TAR
    
    # Tar it locally
    print("Creating Sound Engine Archive...")
    os.system(r'tar -czf sound_engine.tar.gz -C c:\Users\Admin\23226 Sovereign_Sound_Loop')
    
    print("Sending Sound Engine Archive...")
    scp.put('sound_engine.tar.gz', '/root/sovereign/sound_engine.tar.gz')
    ssh.exec_command('cd /root/sovereign && tar -xzf sound_engine.tar.gz && rm sound_engine.tar.gz')
    
    # 4. Ignite Systems
    print("Igniting Systems...")
    commands = [
        'cd /root/sovereign && docker-compose up -d --build',
        'cd /root/sovereign/Sovereign_Sound_Loop && docker-compose up -d --build'
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        print(stderr.read().decode())
    
    scp.close()
    ssh.close()
    print("PATCH DEPLOYED SUCCESSFULLY.")

if __name__ == "__main__":
    deploy_heavy_patch()

import paramiko
import os

def deploy_heavy_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    sftp = ssh.open_sftp()
    
    # 1. Upload Backend Fix
    print("Uploading Backend Fix...")
    sftp.put(r'c:\Users\Admin\23226\backend\main.py', '/root/sovereign/backend/main.py')
    
    # 2. Upload Nginx Config
    print("Uploading Nginx Config...")
    sftp.put(r'c:\Users\Admin\23226\nginx.conf', '/root/sovereign/nginx.conf')
    
    # 3. Create Archive Locally
    print("Creating Sound Engine Archive...")
    # Using full path for tar
    archive_cmd = f'tar -czf sound_engine.tar.gz -C "c:\\Users\\Admin\\23226" Sovereign_Sound_Loop'
    os.system(archive_cmd)
    
    # 4. Upload and Extract
    print("Uploading Sound Engine Archive...")
    sftp.put('sound_engine.tar.gz', '/root/sovereign/sound_engine.tar.gz')
    ssh.exec_command('cd /root/sovereign && tar -xzf sound_engine.tar.gz && rm sound_engine.tar.gz')
    
    # 5. Ignite Systems
    print("Igniting Systems...")
    # We use -d for detached mode. We also prune to keep it clean.
    commands = [
        'cd /root/sovereign && docker-compose up -d --build',
        'cd /root/sovereign/Sovereign_Sound_Loop && docker-compose up -d --build'
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # Read output line by line to show progress
        for line in stdout:
            print(f"STDOUT: {line.strip()}")
        for line in stderr:
            print(f"STDERR: {line.strip()}")
    
    sftp.close()
    ssh.close()
    
    # Cleanup local archive
    if os.path.exists('sound_engine.tar.gz'):
        os.remove('sound_engine.tar.gz')
        
    print("PATCH DEPLOYED SUCCESSFULLY.")

if __name__ == "__main__":
    deploy_heavy_patch()

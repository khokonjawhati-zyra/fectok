import paramiko
import os

def deploy_v15_final_mesh():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=pw)
    
    sftp = ssh.open_sftp()
    
    # Upload Nginx Config
    print("Uploading Nginx Protocol Fix [Resolver 127.0.0.11]...")
    sftp.put(r'c:\Users\Admin\23226\nginx.conf', '/root/sovereign/nginx.conf')
    
    # 2. Hard Stop and Prune
    print("Purging stale containers and orphans...")
    ssh.exec_command('cd /root/sovereign && docker-compose down --remove-orphans')
    
    # 3. Secure Reset + Build
    print("Igniting V15 Master Mesh (Full Cluster Reset)...")
    # Using service names directly. --force-recreate to be 100% sure.
    stdin, stdout, stderr = ssh.exec_command('cd /root/sovereign && docker-compose up -d --build --force-recreate')
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # 4. Check Gateway specifically
    print("Checking Gateway status (Post-Ignition)...")
    stdin, stdout, stderr = ssh.exec_command('docker ps --filter name=sovereign_v15_gateway')
    status = stdout.read().decode()
    if 'Up' in status:
        print("GATEWAY ONLINE: PULSE_POSITIVE.")
    else:
        print("GATEWAY OFFLINE: Retrying start...")
        ssh.exec_command('docker start sovereign_v15_gateway')
    
    sftp.close()
    ssh.close()
    print("MASTER DEPLOYMENT COMPLETE.")

if __name__ == "__main__":
    deploy_v15_final_mesh()

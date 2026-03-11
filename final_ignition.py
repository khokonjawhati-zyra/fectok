import paramiko
import os

def final_ignition():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    local_zip = "sovereign_v1.5.3_final_mirror.zip"
    remote_path = "/root/sovereign"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=120)
        print("CONNECTED. STARTING FINAL MIRROR IGNITION...")
        
        # 1. Upload
        print(f"Uploading {local_zip}...")
        sftp = ssh.open_sftp()
        sftp.put(local_zip, "/root/sovereign_final.zip")
        sftp.close()
        
        # 2. Preparation (Clean and Extract)
        print(f"Preparing {remote_path}...")
        ssh.exec_command(f"rm -rf {remote_path} && mkdir -p {remote_path}")
        stdin, stdout, stderr = ssh.exec_command(f"unzip -o /root/sovereign_final.zip -d {remote_path}")
        stdout.channel.recv_exit_status()
        
        # 3. Inject DEFINITIVE Nginx Config
        print("Injecting definitive Nginx configuration...")
        with open("nginx.conf", "rb") as f:
            nginx_conf_content = f.read()
            
        sftp = ssh.open_sftp()
        with sftp.file(f"{remote_path}/nginx.conf", "wb") as f:
            f.write(nginx_conf_content)
        sftp.close()
        
        # 4. Docker Ignition (Full Restart)
        print("Igniting Docker Ecosystem (Full Stack Restart)...")
        cmds = [
            f"cd {remote_path} && docker compose down",
            f"cd {remote_path} && docker compose up -d --build",
            "docker ps"
        ]
        
        for c in cmds:
            print(f"Exec: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            stdout.channel.recv_exit_status()
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
        print("\n--- SOVEREIGN IS LIVE. MIRROR SYNC V1.5.3 FINAL COMPLETE ---")
    except Exception as e:
        print(f"Error during ignition: {e}")

if __name__ == "__main__":
    final_ignition()

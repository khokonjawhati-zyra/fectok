import paramiko
import os

def upload_v15_smooth_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    files_to_upload = [
        ("c:\\Users\\Admin\\23226\\backend\\main.py", "/root/sovereign/backend/main.py"),
        ("c:\\Users\\Admin\\23226\\sovereign_media_hub\\processor\\processor_engine.py", "/root/sovereign/sovereign_media_hub/processor/processor_engine.py"),
        ("c:\\Users\\Admin\\23226\\sovereign_media_hub\\uplink\\uplink_server.py", "/root/sovereign/sovereign_media_hub/uplink/uplink_server.py"),
        ("c:\\Users\\Admin\\23226\\nginx.conf", "/root/sovereign/nginx.conf")
    ]
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        for local, remote in files_to_upload:
            print(f"Uploading {local}...")
            sftp.put(local, remote)
            
        sftp.close()
        
        print("Restarting Services for Ultra-Smooth Protocol...")
        # Restart Backend, Uplink, and Processor
        ssh.exec_command("docker restart sovereign_v15_backend sovereign_v15_uplink sovereign_v15_processor sovereign_v15_gateway")
        
        print("SUCCESS: V15 Zero-Latency Protocol Injected.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_v15_smooth_patch()

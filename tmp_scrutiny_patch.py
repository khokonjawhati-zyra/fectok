import paramiko
import os

def final_scrutiny_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        sftp = ssh.open_sftp()
        
        print("--- Uploading Final Scrutiny Patch ---")
        sftp.put(r"c:\Users\Admin\23226\nginx.conf", "/root/sovereign/nginx.conf")
        sftp.close()
        
        print("--- Restarting Nginx Gateway ---")
        ssh.exec_command("docker restart sovereign_v15_gateway")
        print("Nginx Gateway Restarted with ABR Optimizations.")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_scrutiny_patch()

import paramiko

def check_cloud():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("--- Storage Mounts (R2 Check) ---")
        stdin, stdout, stderr = ssh.exec_command("df -h | grep s3fs || echo 'R2 NOT MOUNTED'")
        print(stdout.read().decode())
        
        print("--- Cloudflare Config in main.py ---")
        stdin, stdout, stderr = ssh.exec_command("grep -E 'cf_|d1_|kv_' /root/sovereign/backend/main.py")
        print(stdout.read().decode())
        
        print("--- Directory Status ---")
        stdin, stdout, stderr = ssh.exec_command("ls -d /var/www/html/media/videos || echo 'Mount point missing'")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_cloud()

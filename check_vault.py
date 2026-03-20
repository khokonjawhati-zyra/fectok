import paramiko

def check_vault_files():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Checking vault directory on remote server...")
        # Path from EliteSovereignDNA in uplink_server.py
        paths = ["/app/vault/data", "/mnt/sovereign_media", "/var/www/html/media/videos"]
        for p in paths:
             print(f"Checking {p}...")
             stdin, stdout, stderr = ssh.exec_command(f"ls -l {p} | head -n 5")
             print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_vault_files()

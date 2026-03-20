import paramiko
import json

def check_remote_vault():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Check media_vault.json inside docker
        cmd = "docker exec sovereign_v15_backend cat /app/auth_data/media_vault.json | head -n 100"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        print("--- VAULT START ---")
        print(output)
        
        # Check total count
        cmd = "docker exec sovereign_v15_backend cat /app/auth_data/media_vault.json | grep -c '\"file\":'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        count = stdout.read().decode().strip()
        print(f"Total Media Count in Vault: {count}")

        # Check for any .mp3 in 'url' field
        cmd = "docker exec sovereign_v15_backend cat /app/auth_data/media_vault.json | grep '\"url\":' | grep '.mp3'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        mp3_urls = stdout.read().decode().strip()
        print(f"MP3 files in 'url' field:\n{mp3_urls}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_vault()

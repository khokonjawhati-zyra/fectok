import paramiko

def check_remote_files():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Check files in the storage path (docker)
        # /app/vault/data is the path inside backend, which is mapped to some host path
        # Let's find out where it's mapped.
        stdin, stdout, stderr = ssh.exec_command("docker inspect sovereign_v15_backend | grep Source")
        print("--- MOUNT PATHS ---")
        print(stdout.read().decode())
        
        # Check files in /root/sovereign/vault/data (likely host path)
        print("--- FILE LIST ---")
        stdin, stdout, stderr = ssh.exec_command("ls -lh /root/sovereign/vault/data/*.mp4 | head -n 10")
        print(stdout.read().decode())

        # Check a specific file's type using 'file' command
        cmd = "file /root/sovereign/vault/data/grok_video_2026-02-22-15-52-40_1773323035.mp4"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("--- FILE TYPE ---")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_files()

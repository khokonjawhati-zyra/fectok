import paramiko

def check_file_type():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Get first mp4
        cmd = "find /var/www/html/media/videos -name '*.mp4' | head -n 1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        target = stdout.read().decode().strip()
        
        if target:
            print(f"Checking {target}...")
            cmd = f"file {target}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print("File Type:", stdout.read().decode())
            
            # Also check size
            cmd = f"ls -l {target}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print("Size:", stdout.read().decode())
        else:
            print("No mp4 found")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_file_type()

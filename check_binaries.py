import paramiko

def check_binaries():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        for b in ["ffmpeg", "ffprobe", "file"]:
            stdin, stdout, stderr = ssh.exec_command(f"which {b}")
            print(f"{b}: {stdout.read().decode().strip()}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_binaries()

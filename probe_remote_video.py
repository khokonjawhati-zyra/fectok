import paramiko

def probe_remote_video():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Probe first mp4 file found
        cmd = "ls /var/lib/sovereign/vault/data/*.mp4 | head -n 1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        target = stdout.read().decode().strip()
        
        if target:
            print(f"Probing {target}...")
            cmd = f"ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 {target}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
        else:
            print("No .mp4 files found in /var/lib/sovereign/vault/data")

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe_remote_video()

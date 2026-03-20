import paramiko

def probe_uplink_video():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Get first mp4
        cmd = "docker exec sovereign_v15_uplink find /app/vault/data -name '*.mp4' | head -n 1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        target = stdout.read().decode().strip()
        
        if target:
            print(f"Probing {target}...")
            cmd = f"docker exec sovereign_v15_uplink ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 {target}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print("Streams:", stdout.read().decode())
        else:
            print("No mp4 found")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe_uplink_video()

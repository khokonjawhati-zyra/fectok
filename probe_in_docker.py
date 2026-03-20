import paramiko

def probe_in_docker():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # List files in uplink container
        cmd = "docker exec sovereign_v15_uplink ls /var/www/html/media/videos | grep .mp4 | head -n 1"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        target_file = stdout.read().decode().strip()
        
        if target_file:
            print(f"Probing {target_file} inside uplink container...")
            cmd = f"docker exec sovereign_v15_uplink ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 /var/www/html/media/videos/{target_file}"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode().strip()
            print(f"Streams:\n{result}")
        else:
            print("No mp4 found inside uplink container")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    probe_in_docker()

import paramiko

def debug_urls_v2():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Get a file
        stdin, stdout, stderr = ssh.exec_command("ls /var/www/html/media/videos/*.mp4 | head -n 1")
        filename = stdout.read().decode().strip().split("/")[-1]
        
        if not filename:
            print("No video files found!")
            return

        print(f"Testing file: {filename}")
        
        # 1. /video_stream/
        url1 = f"http://localhost/video_stream/stream/{filename}"
        stdin, stdout, stderr = ssh.exec_command(f"curl -I {url1}")
        print(f"\nURL: {url1}")
        print(stdout.read().decode())
        
        # 2. /stream/
        url2 = f"http://localhost/stream/{filename}"
        stdin, stdout, stderr = ssh.exec_command(f"curl -I {url2}")
        print(f"\nURL: {url2}")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_urls_v2()

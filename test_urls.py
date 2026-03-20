import paramiko

def test_internal_urls():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Testing internal proxy to uplink_hub...")
        # Get one recent file from the vault
        stdin, stdout, stderr = ssh.exec_command("ls /var/www/html/media/videos/*.mp4 | head -n 1")
        file_path = stdout.read().decode().strip()
        filename = file_path.split('/')[-1] if file_path else "test.mp4"
        
        print(f"File found: {filename}")
        
        # Test 1: Direct to Uplink Hub
        print(f"Test 1: curl -I http://localhost:8080/stream/{filename}")
        stdin, stdout, stderr = ssh.exec_command(f"curl -I http://localhost:8080/stream/{filename}")
        print(stdout.read().decode())
        
        # Test 2: Through Nginx /video_stream/
        print(f"Test 2: curl -I http://localhost/video_stream/stream/{filename}")
        stdin, stdout, stderr = ssh.exec_command(f"curl -I http://localhost/video_stream/stream/{filename}")
        print(stdout.read().decode())
        
        # Test 3: Through Nginx /stream/
        print(f"Test 3: curl -I http://localhost/stream/{filename}")
        stdin, stdout, stderr = ssh.exec_command(f"curl -I http://localhost/stream/{filename}")
        print(stdout.read().decode())

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_internal_urls()

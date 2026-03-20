import paramiko
import re

def bust_cache_index():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        index_path = "/root/sovereign/webuser_panel/index.html"
        
        stdin, stdout, stderr = ssh.exec_command(f"cat {index_path}")
        content = stdout.read().decode()
        
        # Add a version timestamp to the main.dart.js script
        import time
        v = int(time.time())
        # Flutter web loads via flutter.js or service_worker.js
        # We can add a simple meta tag or just a comment to trigger change
        if "<meta name=\"v15-patch\"" not in content:
            content = content.replace("<head>", f"<head>\n  <meta name=\"v15-patch\" content=\"{v}\">")
        
        # Write back
        tmp_remote = "/tmp/index_busted.html"
        sftp = ssh.open_sftp()
        with sftp.file(tmp_remote, 'w') as f:
            f.write(content)
        sftp.close()
        
        ssh.exec_command(f"mv {tmp_remote} {index_path}")
        print(f"Cache busted index.html with version {v}")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bust_cache_index()

import paramiko
import os

def upload_patch():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    try:
        print(f"Connecting to {host} for SFTP upload...")
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, password=pw)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 1. Upload nginx.conf
        print("Uploading nginx.conf...")
        sftp.put(r"c:\Users\Admin\23226\nginx.conf", "/root/sovereign/nginx.conf")
        
        # 2. Upload webuser_panel contents (Surgical)
        local_user_panel = r"c:\Users\Admin\23226\webuser_panel"
        remote_user_panel = "/root/sovereign/webuser_panel"
        
        print("Uploading webuser_panel artifacts...")
        # We only need to upload the changed files (index.html, main.dart.js, etc.)
        # To be safe, we'll upload the whole folder's children
        for root, dirs, files in os.walk(local_user_panel):
            for d in dirs:
                local_dir = os.path.join(root, d)
                remote_dir = os.path.join(remote_user_panel, os.path.relpath(local_dir, local_user_panel)).replace("\\", "/")
                try:
                    sftp.mkdir(remote_dir)
                except:
                    pass
            for f in files:
                local_file = os.path.join(root, f)
                remote_file = os.path.join(remote_user_panel, os.path.relpath(local_file, local_user_panel)).replace("\\", "/")
                sftp.put(local_file, remote_file)
        
        sftp.close()
        transport.close()
        
        # 3. Restart Docker
        print("Restarting Docker Ecosystem...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=pw)
        ssh.exec_command("cd /root/sovereign && docker-compose down && docker-compose up -d")
        ssh.close()
        
        print("\nPATCH DEPLOYED! V15-NET-SYNC [PRO] IS LIVE.")
        return True
    except Exception as e:
        print(f"PATCH FAILED: {e}")
        return False

if __name__ == "__main__":
    upload_patch()

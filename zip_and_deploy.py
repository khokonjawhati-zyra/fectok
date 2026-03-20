import os
import zipfile
import paramiko
import time

def zip_user_panel():
    zip_name = "user_panel_deploy_v7.zip"
    local_dir = "user_panel/build/web"
    
    if not os.path.exists(local_dir):
        print(f"Path not found: {local_dir}")
        return None
        
    count = 0
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # We want to unzip content directly into the remote folder
                arc_path = os.path.relpath(file_path, local_dir)
                zipf.write(file_path, arc_path)
                count += 1
    print(f"Successfully zipped {count} assets into {zip_name}")
    return zip_name

def deploy_to_live(zip_file):
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    deploy_path = "/root/sovereign/webuser_panel"
    remote_zip = f"/root/sovereign/{zip_file}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=60)
        sftp = ssh.open_sftp()
        
        print(f"Uploading {zip_file}...")
        sftp.put(zip_file, remote_zip)
        sftp.close()
        print("Upload complete.")

        print("Updating live web files...")
        commands = [
            f"mkdir -p {deploy_path}",
            f"rm -rf {deploy_path}/*",
            f"unzip -o {remote_zip} -d {deploy_path}",
            "docker restart sovereign_v15_gateway",
            f"rm {remote_zip}"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        print("Deployment successful!")
        ssh.close()
        return True
    except Exception as e:
        print(f"Deployment Error: {e}")
        return False

if __name__ == "__main__":
    zip_file = zip_user_panel()
    if zip_file:
        deploy_to_live(zip_file)

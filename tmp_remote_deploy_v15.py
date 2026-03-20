import paramiko
import os

def deploy_to_server():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {host}...")
        ssh.connect(host, username=user, password=pw, timeout=30)
        print("Connected!")

        # Step 1: Upload Web Builds
        print("Uploading Web Builds...")
        sftp = ssh.open_sftp()
        sftp.put("sovereign_v15_web.zip", "/root/sovereign/code_web.zip")
        sftp.close()

        # Step 2: Extraction and Deployment
        # Using bash -c to ensure glob expansion (*) works
        print("Deploying Web Assets...")
        cmds = [
            "cd /root/sovereign && rm -rf temp_web && mkdir -p temp_web",
            "cd /root/sovereign && unzip -q code_web.zip -d temp_web",
            "cd /root/sovereign && mkdir -p webuser_panel webadmin_panel",
            "cd /root/sovereign && rm -rf webuser_panel/* && cp -rp temp_web/user_panel/build/web/. webuser_panel/",
            "cd /root/sovereign && rm -rf webadmin_panel/* && cp -rp temp_web/admin_panel/build/web/. webadmin_panel/",
            "cd /root/sovereign && rm -rf temp_web code_web.zip",
            "chmod -R 755 /root/sovereign/webuser_panel /root/sovereign/webadmin_panel"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(f"bash -c '{c}'")
            err = stderr.read().decode()
            if err: print(f"Error executing {c}: {err}")
            out = stdout.read().decode()
            if out: print(out)

        # Step 3: Restart Services
        print("Restarting Services...")
        ssh.exec_command("cd /root/sovereign && docker-compose restart stream_gateway")
        
        print("\n--- DEPLOYMENT SUCCESSFUL ---")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    deploy_to_server()

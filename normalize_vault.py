import paramiko
import json
import os

def normalize_server_data():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        vault_path = "/var/lib/sovereign/auth/media_vault.json"
        print(f"Reading {vault_path}...")
        stdin, stdout, stderr = ssh.exec_command(f"cat {vault_path}")
        content = stdout.read().decode()
        
        if not content:
            print("Vault empty or not found.")
            return
            
        data = json.loads(content)
        changed = False
        
        for item in data:
            for key in ["url", "thumb_url", "sound_url"]:
                if key in item and isinstance(item[key], str):
                    val = item[key]
                    # Remove protocols and hosts, make relative to /stream/ or /video_stream/
                    # If it has :8080/stream/ -> /stream/
                    if ":8080/stream/" in val:
                        item[key] = "/stream/" + val.split(":8080/stream/")[-1]
                        changed = True
                    elif ":8080/" in val:
                         item[key] = "/video_stream/" + val.split(":8080/")[-1]
                         changed = True
                    # Remove fectok.com if present to make it relative
                    if "fectok.com" in val:
                         item[key] = "/" + val.split("fectok.com/")[-1]
                         changed = True

        if changed:
            print("Normalizing media vault data...")
            # Write back
            new_content = json.dumps(data, indent=4)
            # Use a temporary file and mv
            tmp_remote = "/tmp/media_vault.json"
            sftp = ssh.open_sftp()
            with sftp.file(tmp_remote, 'w') as f:
                f.write(new_content)
            sftp.close()
            
            ssh.exec_command(f"mv {tmp_remote} {vault_path}")
            print("Normalization complete.")
        else:
            print("No changes needed in media vault.")

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    normalize_server_data()

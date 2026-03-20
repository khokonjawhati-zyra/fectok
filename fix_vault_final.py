import paramiko
import json

def fix_server_vault_absolute():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        vault_path = "/var/lib/sovereign/auth/media_vault.json"
        
        stdin, stdout, stderr = ssh.exec_command(f"cat {vault_path}")
        data = json.loads(stdout.read().decode())
        
        # Force all paths to be relative /stream/ paths which we know work via Nginx alias
        for item in data:
            for key in ["url", "thumb_url", "sound_url", "hls_url"]:
                if key in item and isinstance(item[key], str) and item[key]:
                    val = item[key]
                    # Extract filename or path after /stream/ or /video_stream/stream/
                    parts = val.split("/stream/")
                    if len(parts) > 1:
                        filename = parts[-1]
                        item[key] = f"https://fectok.com/stream/{filename}"
                    elif "fectok.com" in val: # If it's absolute but doesn't have /stream/ correctly
                        filename = val.split("/")[-1]
                        item[key] = f"https://fectok.com/stream/{filename}"
        
        # Write back
        new_content = json.dumps(data, indent=4)
        tmp_remote = "/tmp/media_vault_fixed.json"
        sftp = ssh.open_sftp()
        with sftp.file(tmp_remote, 'w') as f:
            f.write(new_content)
        sftp.close()
        
        ssh.exec_command(f"mv {tmp_remote} {vault_path}")
        print("Successfully fixed all vault URLs on server.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_server_vault_absolute()

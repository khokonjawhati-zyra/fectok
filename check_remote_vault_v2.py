import paramiko
import json

def check_remote_vault_v2():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        # Get full vault
        cmd = "docker exec sovereign_v15_backend cat /app/auth_data/media_vault.json"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        full_json = stdout.read().decode()
        
        try:
            data = json.loads(full_json)
            print(f"Total items: {len(data)}")
            for m in data:
                url = m.get('url', '')
                f = m.get('file', '')
                if '.mp3' in url.lower() or '.mp3' in f.lower():
                    print(f"BINGO: File={f}, URL={url}")
                elif '.jpg' in url.lower() or '.png' in url.lower():
                     print(f"IMAGE: File={f}, URL={url}")
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            print("Raw start:", full_json[:200])
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_vault_v2()

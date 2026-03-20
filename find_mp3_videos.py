import paramiko
import json

def find_mp3_videos():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        cmd = "docker exec sovereign_v15_backend cat /app/auth_data/media_vault.json"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        full_json = stdout.read().decode()
        
        try:
            data = json.loads(full_json)
            found = []
            for m in data:
                url = m.get('url', '')
                if url.lower().endswith('.mp3'):
                    found.append(m)
            
            print(f"Found {len(found)} items where URL ends with .mp3")
            for m in found:
                print(f"FILE: {m.get('file')} | URL: {m.get('url')}")
        except Exception as e:
            print(f"JSON Error: {e}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_mp3_videos()

import paramiko
import json

def check_hls_status():
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
            for m in data:
                if m.get('file', '').endswith('.mp4'):
                    print(f"File: {m.get('file')} | HLS: {m.get('hls_ready')} | HLS_URL: {m.get('hls_url')}")
        except Exception as e:
            print(f"Error: {e}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_hls_status()

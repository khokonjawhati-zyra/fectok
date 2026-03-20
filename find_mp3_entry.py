import paramiko
import json

def find_mp3_entry():
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
        
        data = json.loads(full_json)
        for m in data:
            if 's_d9814292.mp3' in str(m):
                print(json.dumps(m, indent=4))
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_mp3_entry()

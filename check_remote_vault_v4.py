import paramiko
import json

def check_remote_vault_v4():
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
            for i, m in enumerate(data):
                f = m.get('file', 'N/A')
                u = m.get('url', 'N/A')
                print(f"Index {i}: {f} | {u}")
        except Exception as e:
            print(f"Error: {e}")
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_remote_vault_v4()

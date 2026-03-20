import paramiko
import json

def inspect_gateway():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        cmd = "docker inspect sovereign_v15_gateway --format '{{json .Mounts}}'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        
        mounts = json.loads(output)
        for m in mounts:
            print(f"Type: {m.get('Type')}")
            print(f"Source: {m.get('Source')}")
            print(f"Destination: {m.get('Destination')}")
            print("-" * 20)
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_gateway()

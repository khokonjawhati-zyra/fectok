import paramiko

def map_ips():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("MAPPING CONTAINER IPS...")
        
        stdin, stdout, stderr = ssh.exec_command("docker ps -q | xargs docker inspect -f '{{.Name}}: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    map_ips()

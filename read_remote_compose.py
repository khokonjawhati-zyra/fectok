import paramiko

def read_remote_file(path):
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print(f"Reading {path}...")
        stdin, stdout, stderr = ssh.exec_command(f"cat {path}")
        content = stdout.read().decode()
        
        # Save locally so I can view it
        local_name = path.replace("/", "_").replace(".yml", ".yaml")
        with open("remote_" + local_name, "w") as f:
            f.write(content)
        
        print(f"Saved to remote_{local_name}")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_remote_file("/root/sovereign/docker-compose.yml")

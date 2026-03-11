import paramiko

def find_git_node():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=pw, timeout=30)
        
        stdin, stdout, stderr = ssh.exec_command("find / -name .git -type d -not -path '*/.*' 2>/dev/null")
        print("GIT NODES FOUND:")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    find_git_node()

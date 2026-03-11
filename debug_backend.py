import paramiko

def debug_backend():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("DEBUGGING BACKEND...")
        
        cmds = [
            "docker inspect sovereign_v15_backend --format '{{.State.Status}} {{.State.ExitCode}}'",
            "docker logs sovereign_v15_backend --tail 100"
        ]
        
        for c in cmds:
            print(f"--- {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print("STDOUT:", stdout.read().decode(errors='ignore'))
            print("STDERR:", stderr.read().decode(errors='ignore'))
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_backend()

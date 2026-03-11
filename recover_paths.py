import paramiko

def recover_files():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("RECOVERING FILES...")
        
        # Check where the hell the files are
        cmds = [
            "ls -la /root",
            "ls -la /root/sovereign",
            "find /root -name 'main.py' | head -n 10",
            "find /root -name 'uplink_server.py' | head -n 10"
        ]
        
        for c in cmds:
            print(f"--- RUNNING: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    recover_files()

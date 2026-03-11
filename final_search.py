import paramiko

def final_search():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("SEARCHING FOR COMPONENT ENTRY POINTS...")
        
        cmds = [
            "find /root -name 'main.py' | head -n 5",
            "find /root -name 'uplink_server.py' | head -n 5",
            "ls -F /root/sovereign"
        ]
        
        for c in cmds:
            print(f"--- RESULT FOR: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_search()

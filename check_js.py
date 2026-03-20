import paramiko

def check_file_content():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected.")
        
        # Binary search for the string to avoid encoding issues
        cmd = "grep -a 'SSL-ENFORCED' /root/sovereign/webuser_panel/main.dart.js"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        if result:
            print(f"Found SSL-ENFORCED in main.dart.js (Binary check: {len(result)} bytes)")
        else:
            print("NOT FOUND in main.dart.js")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_file_content()

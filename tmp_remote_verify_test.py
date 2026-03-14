import paramiko

def check_verify_token():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("--- CURL /verify_token from remote ---")
        # Try POST with empty token. Should return REJECTED
        stdin, stdout, stderr = ssh.exec_command("curl -X POST -H 'Content-Type: application/json' -d '{\"token\":\"\"}' http://localhost/verify_token")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_verify_token()

import paramiko

def api_pulse_check():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("DIAGNOSING API ENDPOINTS...")
        
        cmds = [
            # Check if backend is listening on 5000
            "docker exec sovereign_v15_backend netstat -tulpn | grep :5000",
            
            # Direct internal request to backend
            "docker exec sovereign_v15_gateway curl -s -X POST http://backend_node:5000/admin_auth_init",
            
            # External-style request through Nginx (Gateway)
            "curl -s -X POST -H 'Host: vazo.fectok.com' http://localhost/admin_auth_init",
            
            # Check Nginx error logs specifically for the last few minutes
            "docker logs sovereign_v15_gateway --tail 20"
        ]
        
        for c in cmds:
            print(f"--- EXEC: {c} ---")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            print(stderr.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    api_pulse_check()

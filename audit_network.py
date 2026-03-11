import paramiko

def audit_network():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("AUDITING NETWORK MESH...")
        
        cmds = [
            "docker network inspect sovereign_v15_mesh",
            "docker exec sovereign_v15_gateway nslookup backend_node",
            "docker exec sovereign_v15_gateway ping -c 1 backend_node",
            "docker exec sovereign_v15_gateway telnet backend_node 5000", # Telnet test
            "curl -v http://localhost:5000/api/v15/ping" # Localhost test on host
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
    audit_network()

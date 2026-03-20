import paramiko

def monitor_upload_logs():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        print("Monitoring logs of the uplink component...")
        # Assuming uplink is running in a docker container named sovereign_v15_uplink or similar
        # Let's find the container name first
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}}'")
        containers = stdout.read().decode().split()
        
        uplink_container = next((c for c in containers if 'uplink' in c), None)
        if uplink_container:
            print(f"Found uplink container: {uplink_container}")
            stdin, stdout, stderr = ssh.exec_command(f"docker logs --tail 20 {uplink_container}")
            print(stdout.read().decode())
        else:
            print("Uplink container not found. Checking system processes...")
            stdin, stdout, stderr = ssh.exec_command("ps aux | grep uplink_server")
            print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    monitor_upload_logs()

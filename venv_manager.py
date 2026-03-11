import paramiko

def setup_venv():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Setting up Virtual Environment (VENV) to solve dependency issues...")
        
        cmds = [
            # Create a venv
            "cd /root/sovereign/backend && python3 -m venv venv",
            # Install dependencies inside venv
            "/root/sovereign/backend/venv/bin/pip install fastapi uvicorn[standard] motor websockets python-multipart requests",
            "pkill -f uvicorn || true",
            # Start backend using the venv's uvicorn
            "cd /root/sovereign/backend && nohup /root/sovereign/backend/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Use channel to wait for execution
            exit_status = stdout.channel.recv_exit_status()
            print(f"Exit status: {exit_status}")
            if exit_status != 0:
                print(f"ERR: {stderr.read().decode()}")
        
        print("VENV ACTIVATION COMPLETE! VERIFYING PORT 5000...")
        stdin, stdout, stderr = ssh.exec_command("sleep 5 && netstat -tupln | grep 5000")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_venv()

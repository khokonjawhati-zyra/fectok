import paramiko

def indent_medic():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Fixing Indentation Pulses...")
        
        cmds = [
            # 1. Look for 'if watchdog:' and comment it out too if it exists and caused indentation issues
            "sed -i 's/if watchdog:/# if watchdog:/g' /root/sovereign/backend/main.py",
            # 2. Re-verify the file state
            "grep -n 'watchdog' /root/sovereign/backend/main.py | tail -n 5",
            # 3. Final Re-Ignition
            "pkill -f uvicorn || true",
            "cd /root/sovereign/backend && nohup ./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1 &",
            "sleep 5",
            "netstat -tupln | grep 5000"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            print(stdout.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    indent_medic()

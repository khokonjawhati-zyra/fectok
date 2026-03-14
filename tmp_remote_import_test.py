import paramiko

def check_imports():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        
        test_script = """
try:
    print('Testing payout_bridge import...')
    import payout_bridge
    print('payout_bridge OK')
except Exception as e:
    print(f'payout_bridge FAIL: {e}')

try:
    print('Testing imperial_finance import...')
    import imperial_finance
    print('imperial_finance OK')
except Exception as e:
    print(f'imperial_finance FAIL: {e}')
"""
        # Save and run test script inside container
        ssh.exec_command("docker exec sovereign_v15_backend python3 -c \"" + test_script.replace('\n', '; ').replace('\"', '\\\"') + "\"")
        stdin, stdout, stderr = ssh.exec_command("docker exec sovereign_v15_backend python3 -c \"" + test_script + "\"")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_imports()

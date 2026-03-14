import json
import os
import re

def heal_databases():
    auth_dir = "/var/lib/sovereign/auth"
    target_host = "fectok.com"
    
    files = ["media_vault.json", "users_manifest.json", "ledger.json", "content_ownership.json"]
    
    for filename in files:
        path = os.path.join(auth_dir, filename)
        if not os.path.exists(path):
            print(f"Skipping {filename}: Not found.")
            continue
            
        print(f"Healing {filename}...")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Replace any IP (10.x, 172.x, 192.x, or public) or localhost with target_host
            # Also replace 8080/5000/8000 ports if they are attached to fectok.com
            # Note: We use a broad IP regex + localhost
            content = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target_host, content)
            content = content.replace("localhost", target_host)
            
            # 2. Fix Protocols and Ports
            # Replace http://fectok.com:8080 or http://fectok.com with https://fectok.com
            content = re.sub(rf'http://{target_host}(:8080|:5000|:8000|:9900)?', f'https://{target_host}', content)
            
            # 3. Fix Paths for videos
            # Change /stream/ to /video_stream/stream/ unless already changed
            # Be careful not to double prefix
            content = content.replace(f"https://{target_host}/stream/", f"https://{target_host}/video_stream/stream/")
            # Fix double prefixes if they occurred
            content = content.replace("/video_stream/video_stream/", "/video_stream/")
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Healed {filename} successfully.")
            
        except Exception as e:
            print(f"Error healing {filename}: {e}")

if __name__ == "__main__":
    heal_databases()

import os
import zipfile

def zip_web_builds(zip_name):
    # Only include web builds
    paths = [
        ('user_panel/build/web', 'user_panel/build/web'),
        ('admin_panel/build/web', 'admin_panel/build/web')
    ]
    
    count = 0
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for local_dir, remote_prefix in paths:
            if not os.path.exists(local_dir):
                print(f"Path not found: {local_dir}")
                continue
            
            for root, dirs, files in os.walk(local_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.join(remote_prefix, os.path.relpath(file_path, local_dir))
                    zipf.write(file_path, arc_path)
                    count += 1
                    
    print(f"Successfully zipped {count} web assets into {zip_name}")

if __name__ == "__main__":
    zip_web_builds("sovereign_v15_web.zip")

import os
import zipfile

def zip_source_only(zip_name):
    # Exclusion list for light build to keep it under 50MB
    exclude = {'.git', 'build', '.dart_tool', 'node_modules', '__pycache__', '.venv', '.gradle'}
    
    count = 0
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Prune directories in-place
            dirs[:] = [d for d in dirs if d not in exclude]
            
            for file in files:
                # Skip heavy binaries and the script itself
                if file.endswith(('.zip', '.apk', '.exe', '.pyc')): continue
                if file == zip_name: continue
                
                file_path = os.path.join(root, file)
                try:
                    zipf.write(file_path, os.path.relpath(file_path, '.'))
                    count += 1
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")
                    
    print(f"Successfully zipped {count} files into {zip_name}")

if __name__ == "__main__":
    zip_source_only("sovereign_v15_light.zip")

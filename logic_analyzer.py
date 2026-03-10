import os

def get_dir_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except: pass
    return total

if __name__ == "__main__":
    root = "."
    project_parts = {}
    
    # Analyze root level folders
    for d in os.listdir(root):
        p = os.path.join(root, d)
        if os.path.isdir(p):
            project_parts[d] = get_dir_size(p)
        else:
            project_parts[f"[FILE] {d}"] = os.path.getsize(p)

    # Sort and print
    sorted_parts = sorted(project_parts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Target Source':<40} | {'Actual Weight (MB)':<15}")
    print("-" * 60)
    for name, size in sorted_parts:
        if size > 1024 * 1024: # Only show > 1MB
            print(f"{name:<40} | {size / (1024*1024):.2f} MB")

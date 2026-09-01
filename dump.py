import os

# Target directories to dump
TARGET_DIRS = ["pylage", "pylage_layout", "app", "test"]
ROOT_FILES = ["main.py"]  # Markdown & note files removed
OUTPUT_FILE = "project_dump.txt"

# Extensions and keywords to exclude
EXCLUDE_EXTENSIONS = ('.pyc', '.bak', '.v01', '.txt', '.md')
EXCLUDE_DIRS = ('__pycache__', 'test_output', '.venv', '.git')

def generate_tree(startpath):
    """Generate a clean visual ASCII tree of the project."""
    tree_str = "PROJECT DIRECTORY TREE:\n"
    tree_str += "=" * 50 + "\n.\n"
    
    for root, dirs, files in os.walk(startpath):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        subindent = '├── '
        
        if root != startpath:
            tree_str += f"{indent}{subindent}{os.path.basename(root)}/\n"
            
        sub_indent_file = '│   ' * (level + 1)
        for f in sorted(files):
            if not f.endswith(EXCLUDE_EXTENSIONS) and not f.startswith('.before_'):
                tree_str += f"{sub_indent_file}├── {f}\n"
                
    tree_str += "=" * 50 + "\n\n"
    return tree_str

def dump_project():
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_root, OUTPUT_FILE)

    print("🚀 Generating project dump...")

    with open(output_path, "w", encoding="utf-8") as out:
        # 1. Write Directory Tree First
        out.write(generate_tree(project_root))

        # 2. Dump Target Files Content
        file_count = 0
        for root, dirs, files in os.walk(project_root):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            rel_dir = os.path.relpath(root, project_root)
            top_dir = rel_dir.split(os.sep)[0]

            is_target_dir = top_dir in TARGET_DIRS
            is_root_dir = rel_dir == "."

            if not (is_target_dir or is_root_dir):
                continue

            for file in sorted(files):
                # Filter unwanted files
                if file.endswith(EXCLUDE_EXTENSIONS) or file.startswith('.before_'):
                    continue
                if is_root_dir and file not in ROOT_FILES:
                    continue

                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, project_root)

                out.write(f"\n{'=' * 80}\n")
                out.write(f"FILE: {rel_file_path}\n")
                out.write(f"{'=' * 80}\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        out.write(f.read())
                        out.write("\n")
                    file_count += 1
                    print(f"  [+] Added: {rel_file_path}")
                except Exception as e:
                    print(f"  [!] Failed to read {rel_file_path}: {e}")

    print(f"\n✅ Dump complete! Total {file_count} files dumped into '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    dump_project()
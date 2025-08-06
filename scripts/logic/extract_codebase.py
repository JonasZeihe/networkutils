#!/usr/bin/env python3
import os
import sys
import datetime

EXCLUDED_DIRS = {
    "__pycache__", ".git", ".venv", "venv", "build",
    "dist", ".mypy_cache", ".pytest_cache",
}
ALLOWED_SUFFIX = ".py"
ENCODING = "utf-8"


def should_exclude_dir(dirname):
    return dirname in EXCLUDED_DIRS


def gather_python_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
        for file in files:
            if file.endswith(ALLOWED_SUFFIX):
                yield os.path.join(root, file)


def build_tree(path, prefix=""):
    entries = sorted(e for e in os.listdir(path) if not should_exclude_dir(e))
    tree_lines = []
    for index, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree_lines.append(f"{prefix}{connector}{entry}")
        if os.path.isdir(full_path):
            extension = "    " if index == len(entries) - 1 else "│   "
            tree_lines.extend(build_tree(full_path, prefix + extension))
    return tree_lines


def find_target(base_path, target_name):
    for root, dirs, files in os.walk(base_path):
        if target_name in dirs or target_name in files:
            return os.path.join(root, target_name)
    return None


def write_log(log_path, message):
    with open(log_path, "a", encoding=ENCODING) as log:
        log.write(message + "\n")


def collect_and_write_files(target_path, output_path, log_path):
    file_count = 0
    with open(output_path, "w", encoding=ENCODING) as output_file:
        output_file.write("Merged Python source files\n" + "=" * 30 + "\n\n")
        if os.path.isfile(target_path):
            files_to_process = [target_path] if target_path.endswith(ALLOWED_SUFFIX) else []
        else:
            files_to_process = gather_python_files(target_path)

        for file_path in files_to_process:
            try:
                with open(file_path, "r", encoding=ENCODING, errors="ignore") as f:
                    content = f.read()
                output_file.write(f"----- {file_path} -----\n{content}\n{'=' * 30}\n\n")
                write_log(log_path, f"✔ Processed: {file_path}")
                file_count += 1
            except Exception as e:
                write_log(log_path, f"✘ ERROR reading {file_path}: {e}")

    return file_count


def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_path = os.path.join(script_dir, f"{timestamp}_combine_log.txt")

    search_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(script_dir, "..", ".."))
    if not os.path.isdir(search_path):
        print(f"ERROR: Directory does not exist: {search_path}")
        write_log(log_path, f"ERROR: Directory does not exist: {search_path}")
        sys.exit(1)

    print(f"\n📁 Directory structure under '{search_path}':\n")
    tree = build_tree(search_path)
    print("\n".join(tree))

    target_name = input("\n🔍 Enter folder or file name to scan ('exit' to quit): ").strip()
    if target_name.lower() == "exit":
        print("Exiting.")
        sys.exit(0)

    target_path = find_target(search_path, target_name)
    if not target_path:
        print(f"❌ '{target_name}' not found under {search_path}")
        sys.exit(1)

    suffix = target_name.replace(os.sep, "_")
    custom_output_name = f"{timestamp}_{suffix}.txt"
    output_path = os.path.join(script_dir, custom_output_name)

    write_log(log_path, f"Start: {datetime.datetime.now()} | Scanning {target_path}")
    print(f"\n📄 Processing '{target_path}'...\n")

    file_count = collect_and_write_files(target_path, output_path, log_path)

    result = f"{file_count} files processed." if file_count else "No Python files found."
    print(f"\n✅ {result}\nOutput: {output_path}\nLog: {log_path}")
    write_log(log_path, f"Done: {datetime.datetime.now()} | {result}")


if __name__ == "__main__":
    main()

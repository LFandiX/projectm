import os
import hashlib
import json
import argparse


class FileIntegrityChecker:
    def __init__(self, hash_algo="sha256"):
        self.hash_algo = hash_algo
        self.hash_func = getattr(hashlib, hash_algo)

    def compute_hash(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_hash = self.hash_func()
                while chunk := f.read(4096):
                    file_hash.update(chunk)
            return file_hash.hexdigest()
        except Exception as e:
            print(f"Error computing hash for {file_path}: {e}")
            return None

    def scan_directory(self, directory):
        file_hashes = {}
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = self.compute_hash(file_path)
                if file_hash:
                    file_hashes[file_path] = file_hash
        return file_hashes

    def save_hashes(self, file_hashes, output_file):
        with open(output_file, "w") as f:
            json.dump(file_hashes, f, indent=4)

    def load_hashes(self, input_file):
        with open(input_file, "r") as f:
            return json.load(f)

    def verify_files(self, directory, hash_file):
        current_hashes = self.scan_directory(directory)
        stored_hashes = self.load_hashes(hash_file)

        added_files = set(current_hashes.keys()) - set(stored_hashes.keys())
        deleted_files = set(stored_hashes.keys()) - set(current_hashes.keys())
        modified_files = {
            file for file in current_hashes if file in stored_hashes and current_hashes[file] != stored_hashes[file]
        }

        # Verbose report
        print("\nFile Integrity Checker - Verification (Verbose Mode)")
        print("-" * 50)
        print(f"Directory to scan: {directory}")
        print(f"Using hash database: {hash_file}")
        print("\nVerifying files...\n")

        for file in current_hashes:
            if file in added_files:
                print(f"Processing: {file} [New File]")
            elif file in modified_files:
                print(f"Processing: {file} [Modified]")
            else:
                print(f"Processing: {file} [OK]")

        for file in deleted_files:
            print(f"Processing: {file} [Deleted]")

        print("\nVerification Results:")
        print(f"- Total files scanned: {len(current_hashes) + len(deleted_files)}")
        print(f"- Unchanged files: {len(current_hashes) - len(added_files) - len(modified_files)}")
        print(f"- Modified files: {len(modified_files)}")
        print(f"- New files: {len(added_files)}")
        print(f"- Deleted files: {len(deleted_files)}\n")

        # Detailed report
        print("Detailed Report:")
        if modified_files:
            print("\nModified Files:")
            for file in modified_files:
                print(f"1. {file}")
        if added_files:
            print("\nNew Files:")
            for file in added_files:
                print(f"1. {file}")
        if deleted_files:
            print("\nDeleted Files:")
            for file in deleted_files:
                print(f"1. {file}")

        return added_files, deleted_files, modified_files


# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("command", choices=["init", "update", "verify"], help="Action to perform")
    parser.add_argument("--dir", required=True, help="Directory to scan")
    parser.add_argument("--hash_file", default="file_hashes.json", help="File to store/load hashes")
    parser.add_argument("--hash_algo", default="sha256", help="Hash algorithm to use (default: sha256)")

    args = parser.parse_args()
    checker = FileIntegrityChecker(hash_algo=args.hash_algo)

    if args.command == "init":
        hashes = checker.scan_directory(args.dir)
        checker.save_hashes(hashes, args.hash_file)
        print(f"Initialized hash database at {args.hash_file}")

    elif args.command == "update":
        hashes = checker.scan_directory(args.dir)
        checker.save_hashes(hashes, args.hash_file)
        print(f"Updated hash database at {args.hash_file}")

    elif args.command == "verify":
        checker.verify_files(args.dir, args.hash_file)


if __name__ == "__main__":
    main()

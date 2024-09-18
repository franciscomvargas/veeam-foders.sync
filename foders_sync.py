import os
import shutil
import hashlib
import time
import argparse
import logging


def setup_logging(log_file):
    """Set up logging to file and console."""
    logger = logging.getLogger('folder_sync')
    logger.setLevel(logging.INFO)

    # Create a file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def get_file_md5(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class SyncFolders:
    def __init__(self, source_folder, replica_folder, sync_freq, log_file):
        if not os.path.isdir(source_folder):
            raise ValueError("Error: Source directory does not exist.")
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.sync_freq = sync_freq
        # Set up logging
        self.logger = setup_logging(log_file)

    def __sync_folders(self):
        """Synchronize the replica folder to match the source folder."""
        try:
            # Copy files and directories from source folder that aren't in the replica folder
            for dirpath, _, filenames in os.walk(self.source_folder):
                # Calculate the corresponding path in the replica
                relative_path = os.path.relpath(dirpath, self.source_folder)
                replica_path = os.path.join(self.replica_folder, relative_path)

                # Create directories in the replica that don't exist
                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)
                    self.logger.info(f"Created directory: {replica_path}")

                # Copy or update files
                for filename in filenames:
                    source_file = os.path.join(dirpath, filename)
                    replica_file = os.path.join(replica_path, filename)

                    # If the file doesn't exist in the replica, copy it
                    if not os.path.exists(replica_file):
                        shutil.copy2(source_file, replica_file)
                        self.logger.info(f"Copied file: {source_file} to {replica_file}")
                        continue

                    # If the replica file is different, update it
                    if get_file_md5(source_file) != get_file_md5(replica_file):
                        shutil.copy2(source_file, replica_file)
                        self.logger.info(f"Updated file: {source_file} to {replica_file}")

            # Remove files and directories in the replica folder that aren't in the source folder
            for dirpath, _, filenames in os.walk(self.replica_folder, topdown=False):
                # Calculate the corresponding path in the source
                relative_path = os.path.relpath(dirpath, self.replica_folder)
                source_path = os.path.join(self.source_folder, relative_path)

                # Remove files that are not in the source
                for filename in filenames:
                    replica_file = os.path.join(dirpath, filename)
                    source_file = os.path.join(source_path, filename)
                    if not os.path.exists(source_file):
                        os.remove(replica_file)
                        self.logger.info(f"Removed file: {replica_file}")

                # Remove directories that are not in the source
                if not os.path.exists(source_path):
                    os.rmdir(dirpath)
                    self.logger.info(f"Removed directory: {dirpath}")
        except Exception as e:
            self.logger.error(f"Error during synchronization: {e}")

    def __call__(self):
        self.logger.info(f"Folders Synchronization Started! Frequency: {self.sync_freq}s")
        while True:
            self.__sync_folders()
            time.sleep(self.sync_freq)

    def __del__(self):
        self.logger.info("Folders Synchronization Stopped!")


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('source_folder', help='Path to the source folder')
    parser.add_argument('replica_folder', help='Path to the replica folder')
    parser.add_argument('sync_freq', type=int, help='Synchronization frequency in seconds')
    parser.add_argument('log_file', help='Path to the log file')

    args = parser.parse_args()

    # Perform synchronization periodically
    sf = SyncFolders(args.source_folder, args.replica_folder, args.sync_freq, args.log_file)
    sf()

if __name__ == '__main__':
    main()

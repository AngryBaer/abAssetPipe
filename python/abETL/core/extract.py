
import os
import shutil
import tempfile
import threading
import subprocess

import abScan

from config import PipePaths


def from_archive(zip_path: os.PathLike):

    def unzip(zip_path, extract_dir, done_event):
        # Use Python's built-in zipfile module via subprocess for portability
        command = [
            "python", "-m", "zipfile", "-e", zip_path, extract_dir
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print("Unzip failed:", result.stderr)

        done_event.set()

    # Create a hidden temporary directory
    temp_dir = tempfile.mkdtemp(prefix=".unzip_", dir=os.path.dirname(zip_path))

    # Start a thread to unzip the file
    done_event = threading.Event()
    thread = threading.Thread(target=unzip, args=(zip_path, temp_dir, done_event))
    thread.start()
    done_event.wait()  # Wait for extraction to finish

    return temp_dir


def prime_in(source: os.PathLike, pattern: str):
    """Copy files matching the pattern from source to the input directory."""
    # Ensure the PipePaths.IN directory is clean
    for item in abScan.iter_files(PipePaths.IN.value):
        os.remove(item.path)

    # Copy files matching the pattern from source to PipePaths.IN
    for item in abScan.iter_files(source, abScan.make_pattern(pattern)):
        shutil.copy(item.path, os.path.join(PipePaths.IN.value, item.name))


def cleanup(folder_path: os.PathLike):
    """Remove the specified folder and its contents."""
    if (
        not os.path.exists(folder_path)
        or not os.path.isdir(folder_path)
    ):
        return

    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print(f"Error: {e}")

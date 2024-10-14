import os
import sys
import magic
from config_loader import load_config
from summarizer import summarize_file
from summary_saver import save

# Load configuration from config.yaml
config = load_config()

DATA_FOLDER = config.get('data_folder', 'data')
MAX_FILE_SIZE_MB = config.get('max_file_size_mb', 2)
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = config.get('allowed_extensions', {})
EXPECTED_MIME_TYPES = config.get('expected_mime_types', {})
VALID_FILES = []

def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    return os.path.getsize(file_path)

def get_file_extension(file_name):
    """Returns the file extension in lowercase."""
    _, ext = os.path.splitext(file_name)
    return ext.lower()

def get_mime_type(file_path):
    """Returns the MIME type of the file."""
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to detect MIME type for '{file_path}': {e}")

def validate_file(file_path):
    """Validates the file type and size."""
    file_name = os.path.basename(file_path)
    ext = get_file_extension(file_name)
    size = get_file_size(file_path)

    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File size {size / (1024 * 1024):.2f} MB exceeds the {MAX_FILE_SIZE_MB} MB limit.")

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: '{ext}'")

    mime_type = get_mime_type(file_path)
    if mime_type:
        expected_mime = EXPECTED_MIME_TYPES.get(ext)
        if expected_mime and mime_type != expected_mime:
            raise ValueError(f"MIME type mismatch: expected '{expected_mime}', got '{mime_type}'")
    
    VALID_FILES.append(file_path)
    print(f"[INFO] '{file_name}' is valid.")

def main():
    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(f"The data folder '{DATA_FOLDER}' does not exist. Please create it and try again.")

    files = os.listdir(DATA_FOLDER)
    if not files:
        raise RuntimeError(f"No files found in the '{DATA_FOLDER}' folder. Please add files and rerun the program.")

    print(f"[INFO] Validating files in the '{DATA_FOLDER}' folder...\n")
    for file_name in files:
        file_path = os.path.join(DATA_FOLDER, file_name)
        if os.path.isfile(file_path):
            try:
                validate_file(file_path)
            except ValueError as e:
                print(f"❌ '{file_name}': {e}")
        else:
            print(f"⏺️ Skipping '{file_name}': Not a valid file.\n")

    print(f"\n[INFO] Starting summarization process...\n")
    
    for index, url in enumerate(VALID_FILES):
        print(f"[PROCESS] Summarizing file {index + 1}/{len(VALID_FILES)}: '{os.path.basename(url)}'")
        try:
            summary = summarize_file(url)
            print(f"[SUCCESS] Completed summarization for '{os.path.basename(url)}'.")
        except Exception as e:
            print(f"[ERROR] Failed to summarize '{os.path.basename(url)}': {e}")
            continue

        try:
            print(f"[PROCESS] Saving summary of '{os.path.basename(url)}'...")
            save(url, summary)
            print(f"[SUCCESS] Summary for '{os.path.basename(url)}' saved successfully.\n")
        except Exception as e:
            print(f"[ERROR] Failed to save summary for '{os.path.basename(url)}': {e}")

    print("[INFO] Summarization process completed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

import csv
import os
import re
from datetime import datetime
from config_loader import load_config

# Load configuration from config.yaml
config = load_config()

RESULT_FOLDER = config.get('result_folder', 'results')
RESULT_FILE = config.get('result_file', 'summary.csv')
csv_filepath = os.path.join(RESULT_FOLDER, RESULT_FILE)

def prepare_file():
    """Ensures the CSV file exists by creating it if necessary."""
    if not check_csv_exists():
        print(f"[INFO] '{RESULT_FILE}' not found. Creating a new file...")
        create_csv_file()

def check_csv_exists():
    """Checks if the result CSV file already exists."""
    return os.path.isfile(csv_filepath)

def create_csv_file():
    """Creates a new CSV file with the required headers."""
    try:
        with open(csv_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'File Name', 'Summary', 'Created At'])
        print(f"[SUCCESS] Created '{RESULT_FILE}' successfully.")
        return csv_filepath
    except Exception as e:
        raise RuntimeError(f"Error creating '{RESULT_FILE}': {e}")

def prepare_data(url, summary):
    """Prepares the data to be saved in the CSV file."""
    try:
        file_id = get_next_file_id()
        file_name = re.search(r'[^/]+$', url).group(0)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return [file_id, file_name, summary.strip(), created_at]
    except Exception as e:
        raise ValueError(f"Error preparing data for '{url}': {e}")

def get_next_file_id():
    """Calculates the next file ID based on the number of rows in the CSV."""
    try:
        with open(csv_filepath, mode='r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader) - 1  # Subtract header row
            return row_count + 1
    except Exception as e:
        raise RuntimeError(f"Error reading '{csv_filepath}': {e}")

def save_summary_to_csv(data):
    # """Appends a new row of data to the CSV file."""
    # try:
    #     with open(csv_filepath, mode='a', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(data)
    #     print(f"[SUCCESS] Data saved to '{RESULT_FILE}' successfully.")
    # except Exception as e:
    #     raise RuntimeError(f"Error writing to '{csv_filepath}': {e}")
    
    """Updates the summary if the file name exists; otherwise, adds a new row."""
    try:
        updated = False
        rows = []

        # Read the existing CSV content
        with open(csv_filepath, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header row
            for row in reader:
                if row[1] == data[1]:
                    print(f"[INFO] File '{data[1]}' found. Updating summary...")
                    row[2] = data[2]  # Update summary
                    updated = True
                rows.append(row)
                

        # If not updated, add the new data row
        if not updated:
            print(f"[INFO] Adding new entry for '{data[1]}'.")
            rows.append(data)

        # Write back the updated content
        with open(csv_filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"[SUCCESS] Data saved to '{RESULT_FILE}' successfully.")
    except Exception as e:
        raise RuntimeError(f"Error writing to '{csv_filepath}': {e}")


def save(url, summary):
    """Main function to prepare and save the summary data."""
    print(f"[INFO] Preparing to save summary for '{url}'...")
    try:
        prepare_file()
        data = prepare_data(url, summary)
        save_summary_to_csv(data)
    except Exception as e:
        print(f"[ERROR] Failed to save summary: {e}")
        raise

import logging
import csv

# Setup logging to capture information about warnings and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_tbe_file(file_path):
    metadata = {}
    current_tbl = None

    try:
        # Open the TBE file
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)

            # Iterate over each row in the file
            for row in reader:
                if not row:  # Skip empty rows
                    continue

                # Identify section start (BGN)
                if row[0] == 'BGN' and row[1] == 'TBL':
                    current_tbl = {}
                    metadata['TBL'] = current_tbl

                # Identify section end (EOT)
                elif row[0] == 'EOT' and row[1] == 'TBL':
                    current_tbl = None  # End of the TBL section

                elif current_tbl is not None:
                    # Process rows within the TBL section (key-value pairs)
                    if len(row) != 2:  # Ensure valid key-value pair format
                        logging.warning(f"Malformed row in TBL section: {row}")
                        continue

                    key, value = row[0], row[1]
                    if key in current_tbl:
                        logging.warning(f"Duplicate key '{key}' found in TBL section.")
                    current_tbl[key] = value

                else:
                    logging.warning(f"Unexpected row format or missing section: {row}")
                    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error opening file {file_path}: {e}")
        return None

    # Final check for required fields in metadata
    check_missing_metadata(metadata)

    if 'TBL' not in metadata or not metadata.get('TBL'):
        logging.error("No valid metadata found in the file.")
        return None
        
    # Return parsed metadata
    return metadata

def check_missing_metadata(metadata):
    # Define required fields that must be present in the metadata
    required_fields = ['Title', 'Source']
    tbl_section = metadata.get('TBL', {})
    for field in required_fields:
        if field not in tbl_section:  # Checking inside the TBL section
            logging.warning(f"Missing required metadata field: '{field}'")

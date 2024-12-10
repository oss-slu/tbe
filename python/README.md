## isolate_header

This module parses the TBE file and isolates the header information, including global metadata (BGN and EOT attributes) and TBL sections.

### Features:
- **BGN Attributes**: Extracts metadata from the "BGN" section, storing key-value pairs.
- **TBL Sections**: Extracts attributes from each "TBL" section, associating them with the corresponding section name.
- **EOT Attributes**: Extracts metadata from the "EOT" section, similar to BGN.
- **Error Handling**: Handles empty lines, malformed entries, and unknown line types gracefully.
- **Utilities**: Includes helper functions for stripping quotes, splitting CSV lines, and trimming newline characters.

### Functions:
- `parse_tbe_header(filename: str) -> dict`: Parses a TBE file and returns a dictionary containing the parsed header information.

## Setup

1. Clone this repository or download the Python script to your local machine.
   
2. Ensure you have Python 3.x installed. You can check this by running:
   ```bash
   python --version

3. In the terminal, change the current location to the directory where the isolate_header.py file exists:
cd tbe/python/src/functions
Run the code using Python:
python python/src/functions/isolate_header.py sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv


## output_csv

The functionality of output_csv allows exporting TBL data sections into a CSV format. This enables compatibility with other software for tabular data analysis. It ensures the extracted TBL data is stored in a structured format suitable for CSV output, with proper attribute mapping. Logging (e.g., info or warning) is implemented to document issues like empty or malformed sections without interrupting the export process.

Prerequisites:
Dependencies:

1. Python: Version 3.8 or later is required.
   Install Python from the official Python website(https://www.python.org/downloads/).
   Verify installation by running python --version in the terminal.

2. Required Python Packages:
   pandas: For handling tabular data and exporting it to CSV.
   logging: Built-in Python library used for logging warnings and information.

3. Git: Required to clone the repository.
   Install Git from the Git website.
   Verify installation by running git --version.

Setup Instructions:
Step 1: Install Python and Required Libraries
Ensure Python is installed on your system (see Prerequisites).
Open a terminal and install pandas using pip:
pip install pandas

Step 2: Clone the Repository
Clone the repository using Git:
git clone https://github.com/oss-slu/tbe.git
Navigate to the directory containing the output_csv.py file:
cd tbe/python/src/functions

Step 3: Run the Code
In the terminal, change the current location to the directory where the output_csv.py file exists:
cd tbe/python/src/functions
Run the code using Python:
python output_csv.py

Step 4: Check for Output or Logs
Logging Output: If there are issues like empty or malformed sections, warnings are logged directly in the terminal.
CSV Output: If there are no errors, a directory named output_csv is created in the same directory as output_csv.py.
The CSV files are stored in the output_csv directory for further analysis or usage.

Notes:
Ensure all dependencies are correctly installed before running the program.
The logging mechanism provides essential feedback for troubleshooting issues.
For further customization or troubleshooting, review the code comments within output_csv.py.

## output_TBE

The output_TBE.py script is designed to export Python-native data structures into the TBE file format. It ensures the output adheres to the TBE standard, maintaining data integrity and structure. This functionality allows seamless reading, modification, and saving of data without any loss or structural changes, making it suitable for workflows that require consistent and reliable TBE file handling.

# Installation

1. Clone the repository.
2. Ensure Python 3.6 or later is installed on your system.
3. Navigate to the python/src/functions directory and open the output_TBE.py file.

# Usage

1. Place your input file (file.csv) in the sample data/ directory.
2. Update the file_path in output_tbe_file.py to point to the input file:
   file_path = '../../../sample_data/file.csv'
3. Run the script:
   <code>python3 output_TBE.py</code>
   The processed file will be saved in the same directory as output_TBE.py as output_tbe_file.csv.

## read_directory

The read_directory functionality scans a specified directory for .csv files and extracts metadata for each file. The metadata includes file size, creation and modification timestamps, row and column counts, column names, and sample data. The output is saved in a JSON file for easy analysis and reporting.

Prerequisites:
Dependencies:

1. Python: Version 3.8 or later is required.
   Install Python from the official Python website(https://www.python.org/downloads/).
   Verify installation by running python --version in the terminal.

2. Required Python Packages:
   pandas: For handling tabular data and exporting it to CSV.
   logging: Built-in Python library used for logging warnings and information.

3. Git: Required to clone the repository.
   Install Git from the Git website.
   Verify installation by running git --version.

Setup Instructions:
Step 1: Install Python and Required Libraries
Ensure Python is installed on your system (see Prerequisites).No additional packages need to be installed as the script uses built-in libraries.
Open a terminal and install pandas using pip:
pip install pandas

Step 2: Clone the Repository
Clone the repository using Git:
git clone https://github.com/oss-slu/tbe.git
Navigate to the directory containing the read_directory.py file:
cd tbe/python/src/functions

Step 3: Run the Code
In the terminal, change the current directory to the location of the read_directory.py file:
cd tbe/python/src/functions

Update the paths in read_directory.py for the sample_data

Run the code using Python:
python read_directory.py

Step 4: Check for Output or Logs
Logging Output: Issues like missing or malformed files are logged in the terminal.
Metadata Output: A file named read_directory_metadata.json is created in the current directory.
This file contains metadata for each .csv file processed, including:
1.File size, creation and modification timestamps.

2.Number of rows and columns.

3.Column names and sample data (first five rows).

Notes:
Ensure that the directory you specify contains valid .csv files before running the script.
The logging mechanism provides essential feedback for troubleshooting issues.
For further customization or troubleshooting, review the code comments within read_directory.py.

## read_TBE

The read_TBE.py script is designed to parse and extract data from TBE (Tabular Binary Export) files into Python-native data structures. The script extracts metadata, tabular data, attachments, and comments from the file.

# Prerequisites

- Python 3.x installed on your machine.
- No external dependencies required.

# Usage

1. Clone the repository
2. Update the file path (if needed)
3. Run the script - Navigate to the src folder and run <code>python3 read_TBE.py</code>

## strip_header

### CSV Metadata Extraction

This file provides a Python script to extract global metadata from a TBE-style CSV file. The script reads the file(to update the file path name everytime), identifies the global metadata section, and returns the metadata as a dictionary.

### Requirements

- Python 3.x
- No additional libraries are required (standard Python libraries only).
- Navigate to strip_header.py in python/src/functions
- Run python strip_header.py

## unit_tests

(Add your content here)

## validate_TBE

s
(Add your content here)

### Note on Test File Operations
In the test_tbe_file_operations.py, the first part of the code, which includes the function def test_read_tbe_file_valid():, can be removed later if needed. Additionally, the files ebs_read_tbe.py and bdf_utils.py can also be removed if required. These files are copies of the original files.


#### File Origin Information
###### Current Files:
python/src/functions/ebs_read_tbe.py
python/src/functions/bdf_utils.py

###### Original Source Files:
python_tbe_archive/python_conv/ebs_read_tbe.py
python_tbe_archive/python_conv/bdf_utils.py

#### Testing for read_TBE.py
The testing for python/src/functions/read_TBE.py is commented out in the test_tbe_file_operations.py file to avoid merge conflicts during development.
It can be added back in the future if needed.
As of December 9, 2024, all the tests for read_TBE.py are passing successfully.


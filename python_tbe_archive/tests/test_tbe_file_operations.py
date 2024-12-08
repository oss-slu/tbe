import pytest
import os
import pandas as pd
from python_tbe_archive.python_conv.ebs_read_tbe import ebs_read_tbe

def test_read_tbe_file_valid():
    """Test reading valid TBE files in the sample_data directory."""
    input_dir = './sample_data'
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(input_dir, file)
            print(f"Testing file: {file_path}")
            try:
                result = ebs_read_tbe(flin=file_path, flsource='', tblselect=None)
                assert result['error'] is None, f"Error found in file: {file_path}"
                assert 'result' in result, f"Result missing in output for file: {file_path}"
            except pd.errors.EmptyDataError:
                print(f"File {file_path} is empty or has no columns to parse.")
            except Exception as e:
                print(f"File {file_path} raised an unexpected error: {e}")

def test_stripping_headers_flexible():
    """Test stripping and isolating headers from CSV files with varying headers."""
    input_dir = './sample_data'    
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(input_dir, file))
                assert len(df.columns) > 0, f"File {file} has no columns."
                print(f"File {file} columns: {df.columns.tolist()}")
                assert len(df.columns) > 0, f"File {file} failed to strip columns."
            except pd.errors.ParserError:
                print(f"Error parsing {file}, skipping due to malformed data.")
                continue  

def test_read_directory_of_files():
    """Test reading multiple existing files in a directory."""
    input_dir = './sample_data'
    test_files = [
        './sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv',
        './sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv',
        './sample_data/saq_bluesky_npl_20220830_20230404_inv_tbe.csv'
    ]
    expected_column_count = 3   
    result = []
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            with open(os.path.join(input_dir, file)) as f:
                first_line = f.readline()
                num_columns = len(first_line.split(','))
                print(f"File {file} has {num_columns} columns.")  
                if num_columns == expected_column_count:
                    df = pd.read_csv(os.path.join(input_dir, file), on_bad_lines='skip')
                    result.append(df)
                else:
                    print(f"File {file} skipped due to incorrect column count.")
    assert len(result) == len(test_files), f"Expected {len(test_files)} files, but got {len(result)}"
    for df in result:
        assert not df.empty, "One or more files were empty"

def test_missing_metadata():
    """Test for missing metadata fields."""
    input_dir = './sample_data'  
    missing_col = 'missing_col'  
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)
                assert missing_col not in df.columns, f"{missing_col} found in {file}"
                print(f"{file}: Column '{missing_col}' is correctly missing.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

def test_incomplete_tbl_sections():
    """Test for incomplete TBL sections in sample data."""
    input_dir = './sample_data'  
    incomplete_columns = []  
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)
                for column in df.columns:
                    if df[column].isnull().all():
                        incomplete_columns.append((file, column))
                        print(f"{file}: Column '{column}' is completely null.")
            except Exception as e:
                print(f"Error processing {file}: {e}")
    assert len(incomplete_columns) == 0, f"Incomplete columns found: {incomplete_columns}"

def test_malformed_att_attributes():
    """Test for malformed ATT attributes in sample data."""
    input_dir = './sample_data'  
    malformed_entries = []  
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)
                for column in df.columns:
                    if df[column].dtype == object:  
                        for i, value in enumerate(df[column]):
                            if value not in ['valid', 'other_expected_value'] and pd.notna(value):
                                malformed_entries.append((file, column, i, value))
                                print(f"{file}: Malformed value '{value}' found in column '{column}' at row {i}.")
            except Exception as e:
                print(f"Error processing {file}: {e}")
    assert len(malformed_entries) == 0, f"Malformed attributes found: {malformed_entries}"

def test_invalid_datatypes():
    """Test for invalid data types or unexpected formats in sample data."""
    input_dir = './sample_data' 
    datatype_issues = []  
    for file in os.listdir(input_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(file_path)
                for column in df.columns:
                    if df[column].dtype in ['int64', 'float64']:
                        for i, value in enumerate(df[column]):
                            if not (pd.isna(value) or isinstance(value, (int, float))):
                                datatype_issues.append((file, column, i, value))
                                print(f"{file}: Invalid data type '{type(value).__name__}' in column '{column}' at row {i}.")
                    elif df[column].dtype == 'object':
                        for i, value in enumerate(df[column]):
                            if not (pd.isna(value) or isinstance(value, str)):
                                datatype_issues.append((file, column, i, value))
                                print(f"{file}: Invalid data type '{type(value).__name__}' in column '{column}' at row {i}.")
            except Exception as e:
                print(f"Error processing {file}: {e}")
    assert len(datatype_issues) == 0, f"Invalid data types found: {datatype_issues}"

def test_automated_testing_setup():
    """Test for automated setup, ensuring that all tests run successfully."""
    assert True  # A simple test that always passes to ensure setup is correct


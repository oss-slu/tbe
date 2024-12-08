"""
    Read tbe file

    Parameters:
    - flin: File name 
    - flsource: Source: 'extdata' or directory 
    - tblselect: Null: Read all tables, or name of table to read

    Returns:
    - result: Dictionary of dataframes with tables and metadata, error: Error Message

    Variable Descriptions:
    - tf: Temporary dataframe used to store the CSV data.
    - tf_codes: Stores the first three characters of the first column in the CSV.
    - tf_description: Stores the rest of the content in the first column after the first three characters.
    - itbl_header: Indices where tables start (i.e., where 'TBL' is found).
    - ntables: Number of tables in the CSV.
    - iheader: Index of the current table header.
    - tbl_str: Table name in lowercase.
    - ilast: Last possible row in the current table.
    - ieot: Index of 'EOT' in the current table.
    - iend: Index of the end of data in the current table.
    - istart: Index of the start of data in the current table.
    - ndata: Number of data rows in the current table.
    - hdr_all: All column headers in the current table.
    - tbl_name: Current table name.
    - hdr_select: Column indices that have headers (non-empty).
    - hdr: Selected column headers for the current table.
    - hdr_data: Data column headers for the current table.
    - itbl_sites: Index of 'TBL Sites'.
    - ibgn: Index of 'BGN'.
    - iatt_start: Index to start searching for 'ATT'-prefixed rows.
    - iatt_end: Index to end searching for 'ATT'-prefixed rows.
    - att_indices: Boolean series where True indicates the row starts with 'ATT'.
    - iatt: Index of the first 'ATT'-prefixed row.
    - iatt1: Adjusted index of the first 'ATT'-prefixed row considering the header.
    - iatt2: Adjusted index of the last 'ATT'-prefixed row considering the header.
    - natt: Number of 'ATT'-prefixed rows.
    - att: Metadata (i.e., 'ATT'-prefixed rows) of the current table.
    - att_trans: Transposed version of att.
    - tf_tbl: Data of the current table.
    - tf_tbl_codes: First three characters of tf_tbl's first column.
    - icmt: Boolean series where True indicates the row is a comment.
    - ncmt: Number of comment rows.
    - tb_gbl: Transposed version of tf_tbl if the current table is 'global'.
    - result: Final output containing all tables and corresponding metadata.
    """
import pandas as pd
import re
from tzlocal import get_localzone
from pytz import all_timezones

from .bdf_utils import get_attribute_check

def ebs_read_tbe(flin='./Dku_bluesky_analysis/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv', flsource='extdata', tblselect=None):

    result = {}  # initialize output

    tf = pd.read_csv(flin, header=None, sep=',', usecols=[0, 1], keep_default_na=False)
    nrecs = len(tf)
    print("tf: ", tf)
    tf_codes = tf[0].str[:3]
    print("tf_codes: \n", tf_codes)
    tf_description = tf[0].str[4:]
    print("tf_description: \n", tf_description)
    itbl_header = tf_codes[tf_codes == 'TBL'].index
    ntables = len(itbl_header)
    print("ntables \n", ntables)

    for ntbl in range(1, ntables + 1):
        att_trans = None
        iheader = itbl_header[ntbl - 1]
        tbl_str = tf_description[iheader].lower()
        if tblselect is not None and tbl_str != tblselect.lower():
            print(f'Skipping table {tbl_str}')
            continue

        if ntbl < ntables:
            ilast = itbl_header[ntbl] - 1
        else:
            ilast = nrecs

        ieot = (tf_codes[(iheader + 1):ilast] == 'EOT').idxmax()
        skipdata = False
        if pd.notnull(ieot):
            iend = iheader + ieot
        else:
            inotblank = ((tf[1][(iheader + 1):ilast] != '') & (tf[0][(iheader + 1):ilast] == '')).idxmax()
            if pd.notnull(inotblank):
                iend = iheader + inotblank
                print(f'EOT not found for table {ntbl}/{ntables}, using iend = {iend}')
            else:
                inotblank2 = (tf[1][(iheader + 1):ilast] != '').idxmax()
                if pd.notnull(inotblank2):
                    iend = iheader + inotblank2
                    print(f'Found metadata but no data for table {ntbl}/{ntables}, using iend = {iend}')
                    skipdata = True
                else:
                    print(f'No data and no metadata found for table {ntbl}/{ntables} (consider fixing your file)')
                    continue

        if skipdata:
            istart = iend + 1
            ndata = 0
        else:
            ibgn = (tf_codes[(iheader + 1):iend] == 'BGN').idxmax()
            if pd.notnull(ibgn):
                istart = iheader + ibgn
            else:
                iblank = (tf[0][(iheader + 1):iend] == '').idxmax()
                if pd.notnull(iblank):
                    istart = iheader + iblank
                else:
                    istart = iend
                    print(f'BGN not found for table {ntbl}/{ntables}, using istart = {istart}')
            ndata = iend - istart + 1

        hdr_all = pd.read_csv(flin, header=None, sep=',', skiprows=iheader, nrows=1, keep_default_na=False)
        tbl_name = hdr_all[0].str.replace('^TBL ', '')
        tbl_name = tbl_name.str.replace('\s', '_')
        hdr_select = hdr_all.columns[~hdr_all.isna().any()]
        hdr = hdr_all[hdr_select].reset_index(drop=True)
        hdr[0] = 'TBL_' + tbl_name
        print("tbl_name debug:", tbl_name)
        hdr_data = hdr_all[hdr_select].reset_index(drop=True)

        itbl_sites = (tf[0] == 'TBL Sites').idxmax()
        # print("itbl_sites: ", itbl_sites)
        ibgn = (tf[0][itbl_sites:] == 'BGN').idxmax()

        if pd.notnull(itbl_sites) and pd.notnull(ibgn):
            iatt_start = itbl_sites + 1
            iatt_end = ibgn - 1
            print("iatt_start: ", iatt_start)
            print("iatt_end: ", iatt_end)
            print("tf_codes[iatt_start:iatt_end]: ",tf_codes[iatt_start:iatt_end] )
            att_indices = tf_codes[iatt_start:iatt_end].str.startswith('ATT')

            if not att_indices.any():
                print(f"No 'ATT' rows found between 'TBL Sites' and 'BGN' for table {ntbl}/{ntables}")
                continue

            iatt = att_indices.idxmax()
        else:
            print(f"'TBL Sites' or 'BGN' row not found for table {ntbl}/{ntables}")
            if pd.notnull(iatt):
                iatt1 = iatt + iheader
                iatt2 = iheader + (tf_codes[(iheader + 1):(istart - 1)] == 'ATT').last_valid_index()
                natt = iatt2 - iatt1 + 1
                att = pd.read_csv(flin, header=None, sep=',', skiprows=iatt1, nrows=natt, usecols=hdr_select,
                                keep_default_na=False)
                att.columns = hdr.iloc[0]
                att = att.iloc[iatt - iatt1]
                att.columns = hdr_data.iloc[0]
                att_trans = att.transpose().reset_index()
                att_trans.columns = att_trans.iloc[0]
                att_trans = att_trans[1:]
                att_trans.columns.values[0] = 'Variable'
            else:
                print(f'No attributes found for Table {ntbl}/{ntables}')
                att_trans = None

        if ndata > 0:
            tf_tbl = pd.read_csv(flin, header=None, sep=',', skiprows=istart, nrows=ndata, usecols=hdr_select,
                                 keep_default_na=False)
            tf_tbl_codes = tf_tbl[0].str[:3]
            icmt = tf_tbl_codes == 'CMT'
            ncmt = icmt.sum()
            if ncmt > 0:
                print(f'Removing {ncmt} comments from table {tbl_str}')
                tf_tbl = tf_tbl[~icmt]
            tf_tbl.drop(columns=0, inplace=True)
            tf_tbl.columns = hdr_data.columns[:len(tf_tbl.columns)]
            for col in tf_tbl.columns:
                rtn = get_attribute_check(att_trans, col, 'Units')
                if rtn is None or pd.isnull(rtn['result']):
                    continue
                if tf_tbl[col].dtype == 'datetime64[ns]':
                    tzone = re.match(r'Time\s*\(\s*(.*)\s*\)', rtn['result'])
                    if tzone:
                        tzone = tzone.group(1)
                        if tzone in all_timezones:
                            print(f'Found valid time and timezone ({tzone}) for column {col}')
                            tf_tbl[col] = tf_tbl[col].dt.tz_localize(get_localzone()).dt.tz_convert(tzone)
                        else:
                            print(f'Invalid timezone ({tzone}) for column {col}, leave as is')
                    elif rtn['result'] in all_timezones:
                        tzone = rtn['result']
                        print(f'Inferred time, found timezone ({tzone}) for column {col}')
                        tf_tbl[col] = tf_tbl[col].dt.tz_localize(get_localzone()).dt.tz_convert(tzone)
                    else:
                        print(f'WARNING: No timezone found for variable {col}, leave as is')
                else:
                    continue
        else:
            tf_tbl = None

        if tf_tbl is None:
            print(f"Data for table {tbl_str} is None")
            result[tbl_str] = None
        elif tbl_str.lower() == 'global':
            tb_gbl = tf_tbl.transpose().reset_index()
            result[tbl_str] = tb_gbl.rename(columns={0: 'Variable'})
        
        if att_trans is None:
            print(f"Metadata for table {tbl_str} is None")
            result['tc_' + tbl_str] = tf_tbl
        else:
            result['tc_' + tbl_str] = att_trans
        print(f'Added tables {tbl_str} and tc_{tbl_str} to the result dictionary')

        print(f'Tables {tbl_str} and tc_{tbl_str} for table {ntbl}/{ntables}: {tf_description[iheader]}')
        if ndata > 0:
            print(f'  Rows: header at {iheader}, data from {istart} to {iend}')
        elif att_trans is not None:
            print(f'  Rows: header at {iheader}, metadata only from {iatt1} to {iatt2}')
        else:
            print(f'  Rows: header only at {iheader}, no data, no metadata')

    print(f'Finished reading file: {flin}')
    print('**************** END OF EBS_READ_TBE *************')
    print(f'************************************************** \n\n')
    print(result)
    return {'result': result, 'error': None}


if (__name__ == "__main__"):
    ebs_read_tbe()

import re
import pandas as pd
import numpy as np

def printf(*args):
    """
    Send sprintf output to the screen

    Part of bdf_utils collected from different sources.

    Parameters:
    - args: Arguments passed directly to sprintf

    Returns:
    - The string that was just printed

    Family: bdf_utils
    """
    print(*args, "\n")

def saq_sitename2id(stname=''):
    """
    Make siteid from sitename by removing special characters and shortening
    siteid is lower case, snake case

    Returns:
    - Shortened site name for use in programming

    Family: bdf_utils
    """
    stid = stname.lower()
    stid = re.sub(r'[.,\'() /-]+', '_', stid)
    stid = re.sub(r'(?i)_of_', '_', stid)
    stid = re.sub(r'(?i)university', 'u', stid)
    stid = re.sub(r'(?i)univ', 'u', stid)
    stid = re.sub(r'(?i)airport', 'apt', stid)
    stid = re.sub(r'(?i)campus', '', stid)
    stid = re.sub(r'(?i)school', '', stid)
    stid = re.sub(r'_+$', '', stid)
    stid = re.sub(r'^_+', '', stid)
    stid = re.sub(r'_+', '_', stid)
    stid = re.sub(r'cox_s', 'cox', stid)  # shorten cox_s_bazar to cox_bazar
    return stid

def get_attribute(tc=[('date','pm25','pm10'),
                      ('Asia/Dhaka','ug/m3','ug/m3'),
                      ('Local Time','PM2.5','PM10')],
                  varselect='pm25',
                  attselect='Units'):
    """
    Get attribute from tibble with metadata, return attribute or empty string

    Parameters:
    - tc: Tibble with metadata (attributes)
    - varselect: Row entry to select inside tibble (assumes names are in Variable)
    - attselect: Attribute to select

    Returns:
    - Attribute or ''

    Family: bdf_utils
    """
    tc_df = pd.DataFrame(tc, columns=['Variable', 'Units', 'DisplayName'])
    if 'Variable' not in tc_df.columns:
        return ''
    if attselect not in tc_df.columns:
        return ''
    tcf = tc_df[tc_df['Variable'] == varselect]
    if tcf.shape[0] == 0:
        return ''
    elif tcf.shape[0] > 1:
        return ''
    var_attribute = tcf[attselect].iloc[0]
    return var_attribute

def get_attribute_check(tc=[('date','pm25','pm10'),
                            ('Asia/Dhaka','ug/m3','ug/m3'),
                            ('Local Time','PM2.5','PM10')],
                        varselect='pm25',
                        attselect='Units'):
    """
    Get attribute from tibble with metadata with checking and diagnostics

    Parameters:
    - tc: Tibble with metadata (attributes)
    - varselect: Row entry to select inside tibble (assumes names are in Variable)
    - attselect: Attribute to select

    Returns:
    - result: attribute value, error: Error code if failed

    Family: bdf_utils
    """
    tc_df = pd.DataFrame(tc, columns=['Variable', 'Units', 'DisplayName'])
    if 'Variable' not in tc_df.columns:
        return {'result': None, 'error': f'Could not find Variable in input tibble for get_attribute_check'}
    if attselect not in tc_df.columns:
        return {'result': None, 'error': f'Could not find attribute {attselect} in input tibble for get_attribute_check'}
    tcf = tc_df[tc_df['Variable'] == varselect]
    if tcf.shape[0] == 0:
        return {'result': None, 'error': f'Could not find entry for {varselect} in input tibble for get_attribute_check'}
    elif tcf.shape[0] > 1:
        return {'result': None, 'error': f'Found multiple ({tcf.shape[0]}) entries for {varselect} in input tibble for get_attribute_check'}
    var_attribute = tcf[attselect].iloc[0]
    return {'result': var_attribute, 'error': None}

def df_transpose(df):
    """
    Transpose a tibble, e.g., for writing to file

    Parameters:
    - df: Input tibble

    Returns:
    - Transposed tibble

    Family: bdf_utils
    """
    first_name = df.columns[0]
    if df[df.duplicated(subset=first_name)].any():
        df[first_name] = pd.Series(df[first_name]).astype(str).apply(pd.Series.unique).apply(lambda x: '_'.join(x))
        printf('Made unique names in df_transpose:')
        print(df)
    df_inum = df.select_dtypes(include=np.number).columns
    if len(df_inum) > 0:
        df[df_inum] = df[df_inum].astype(str)
    dft = df.melt(id_vars=[first_name]).pivot(index=first_name, columns='variable', values='value')
    dft.columns.name = None
    return dft

def is_wholenumber(x, tol=np.sqrt(np.finfo(float).eps)):
    """
    Check if a number is an integer

    Parameters:
    - x: Number to be compared to machine precision
    - tol: Tolerance for integer determination

    Returns:
    - logical: True if the number is an integer within machine tolerance

    Family: bdf_utils
    """
    return np.abs(x - np.round(x)) < tol

def clear_viewer_pane():
    """
    Clear all viewer objects

    This is the equivalent of using dev.off() for plots.

    Family: bdf_utils
    """
    dir_path = tempfile.mkdtemp()
    text_file = os.path.join(dir_path, "blank.html")
    with open(text_file, 'w') as file:
        file.write('')
    rstudioapi.viewer(text_file)

def addLegend_decreasing(map, position='topright', pal=None, values=None, na_label="NA", bins=7, colors=None,
                         opacity=0.5, labels=None, labFormat=None, title=None, className="info legend",
                         layerId=None, group=None, data=None, decreasing=False):
    """
    Get leaflet legend to have the minimum value at the bottom

    Replace addLegend(...) with addLegend_decreasing(..., decreasing=True)

    Parameters:
    - map: Leaflet map object
    - position: Position of the legend (default: 'topright')
    - pal: Color palette function
    - values: Values to be mapped
    - na_label: Label for NA values
    - bins: Number of bins
    - colors: Custom colors for the legend
    - opacity: Opacity of the legend
    - labels: Custom labels for the legend
    - labFormat: Format of the labels
    - title: Title of the legend
    - className: CSS class name for the legend
    - layerId: Layer ID
    - group: Group ID
    - data: Data object
    - decreasing: Whether to reverse the order of the legend

    Returns:
    - None
    """
    position = ['topright', 'bottomright', 'bottomleft', 'topleft'][position]
    type = "unknown"
    na_color = None
    extra = None

    if pal is not None:
        if colors is not None:
            raise ValueError("You must provide either 'pal' or 'colors' (not both)")
        if title is None and isinstance(values, pd.Series):
            title = values.name

        values = values.apply(evalFormula, args=(data,))
        type = pal.colorType
        args = pal.colorArgs
        na_color = args.get('na.color', None)
        if na_color is not None and np.array(col2rgb(na_color, alpha=True))[3] == 0:
            na_color = None

        if type == "numeric":
            cuts = np.linspace(values.min(), values.max(), bins)
            if decreasing:
                colors = pal(np.append(np.flip(cuts[:-1]), values.max()))
                labels = labFormat("numeric", np.flip(cuts))
            else:
                colors = pal(np.append(cuts[:-1], values.max()))
                labels = labFormat("numeric", cuts)
        elif type == "bin":
            cuts = args['bins']
            if decreasing:
                colors = pal(np.flip((cuts[1:] + cuts[:-1]) / 2))
                labels = labFormat("bin", np.flip(cuts))
            else:
                colors = pal((cuts[1:] + cuts[:-1]) / 2)
                labels = labFormat("bin", cuts)
        elif type == "quantile":
            p = args['probs']
            cuts = values.quantile(p)
            mids = (cuts[1:] + cuts[:-1]) / 2
            if decreasing:
                colors = pal(np.flip(mids))
                labels = labFormat("quantile", np.flip(cuts), p)
            else:
                colors = pal(mids)
                labels = labFormat("quantile", cuts, p)
        elif type == "factor":
            v = np.sort(values.dropna().unique())
            if decreasing:
                colors = pal(np.flip(v))
                labels = labFormat("factor", np.flip(v))
            else:
                colors = pal(v)
                labels = labFormat("factor", v)
    else:
        if len(colors) != len(labels):
            raise ValueError("'colors' and 'labels' must be of the same length")
    legend = {
        "colors": colors,
        "labels": labels,
        "na_color": na_color,
        "na_label": na_label,
        "opacity": opacity,
        "position": position,
        "type": type,
        "title": title,
        "extra": extra,
        "layerId": layerId,
        "className": className,
        "group": group
    }
    map.addLegend(legend)

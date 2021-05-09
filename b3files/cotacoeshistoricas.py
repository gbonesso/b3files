import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from datetime import datetime
import os
import zipfile
import logging

# Here we'll specify the columns width
__widths = [2, 8, 2, 12, 3, 12,
            10, 3, 4, 13, 13, 13, 13, 13, 13, 13, 5, 18,
            18, 13, 1, 8, 7, 13, 12, 3]

# and the columns names, based in the original specification
__column_names = [
    'TIPREG',  # Tipo de Registro - Fixo = "01"
    'DATPRE',  # Data do pregão - "AAAAMMDD"
    'CODBDI',  # Código BDI - Precisa de tabela auxiliar
    'CODNEG',  # Código de negociação do papel
    'TPMERC',  # Tipo de mercado - (Vista, Termo, etc...) Precisa de tabela auxiliar
    'NOMRES',  # Nome resumido da empresa emissora do papel
    'ESPECI',  # Especificação do papel - (ON, PN, LFT, etc...) Precisa de tabela auxiliar
    'PRAZOT',  # Prazo em dias do mercado a termo
    'MODREF',  # Moeda de referência usada na data do pregão
    'PREABE',  # Preço de abertura do papel no pregão
    'PREMAX', 'PREMIN', 'PREMED', 'PREULT', 'PREOFC', 'PREOFV',
    'TOTNEG', 'QUATOT', 'VOLTOT', 'PREEXE', 'INDOPC', 'DATVEN', 'FATCOT', 'PTOEXE',
    'CODISI', 'DISMES']


def _convert_price(raw_price):
    """Convert the prices, adjusting for two decimals while loading the raw file.
    Parameters:
       raw_price (str): The price to be converted, the last two characters are the decimals.
    Returns:
       (float64): Converted price.
    """
    return float(raw_price) / 100.0


def _convert_date(d):
    """Convert the raw date information.
    The raw file uses '9999' in the year to indicate an invalid year.
    Parameters:
       d (str): The field format is 'YYYYMMDD'.
    Returns:
       dt (datetime64): Decoded date.
    """
    if d.startswith('9999'):
        return None
    try:
        dt = datetime.strptime(d, '%Y%m%d')
        return dt
    except ValueError:
        return None


# Specify dtype while loading
__dtype_dict = {
    'TOTNEG': np.int32
}

# Use the functions defined above to convert data while loading
__convert_dict = {
    'DATPRE': _convert_date,
    'PREABE': _convert_price, 'PREMAX': _convert_price,
    'PREMIN': _convert_price,
    'PREMED': _convert_price, 'PREULT': _convert_price, 'PREOFC': _convert_price,
    'PREOFV': _convert_price,
    'DATVEN': _convert_date,
}


def load_dir(dir_base):
    """Loads all the raw files in a given directory.
    Parameters:
       dir_base (str): inform the path of the directory to be loaded
    Returns:
       df: a dataframe with the decoded data
    """

    df = pd.DataFrame()  # Creates an empty Dataframe to append all the raw files
    logging.debug('load_dir::dir_base: {}'.format(dir_base))

    for dir_name, _, filenames in os.walk(dir_base):
        for filename in filenames:
            logging.debug(os.path.join(dir_name, filename))
            '''z_file = zipfile.ZipFile(os.path.join(dir_name, filename))
            files = z_file.namelist()
            with z_file.open(files[0]) as raw_file:
                # logging.debug(raw_file.readline())  # o readline() muda o ponteiro do arquivo? Estava perdendo duas linhas de dados?
                # logging.debug(raw_file.readline())
                df_temp = load_file(raw_file)'''
            df_temp = load_zipfile(os.path.join(dir_name, filename))
            logging.debug('File: {} #rows: {}'.format(
                os.path.join(dir_name, filename), df_temp.shape[0]))  # shape[0] = Number of rows...
            df = df.append(df_temp, ignore_index=True)

    logging.debug('Total df rows: {}'.format(df.shape[0]))
    return df


def load_zipfile(zip_file_path):
    """Loads one zipped file
    Parameters:
       zip_file_path (str): inform the path of the zipped file to be loaded
    Returns:
       df: a dataframe with the decoded data
    """

    # df = pd.DataFrame()  # Creates an empty Dataframe to append all the raw files
    logging.debug('load_zipfile::zip_file_path: {}'.format(zip_file_path))

    z_file = zipfile.ZipFile(os.path.join(zip_file_path))
    files = z_file.namelist()
    with z_file.open(files[0]) as raw_file:
        df = load_file(raw_file)

    return df


def load_file(file_path):
    """Loads the raw file.
    Parameters:
       file_path (str): inform the file path of the raw file to be loaded
    Returns:
       df: a dataframe with the decode data
    """
    df = pd.read_fwf(
        file_path,
        widths=__widths,
        names=__column_names,
        dtype=__dtype_dict,
        converters=__convert_dict,
        skiprows=1,  # Skip the header row
        skipfooter=1  # Skip the footer row
    )
    return df

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import zipfile
import logging


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


# TODO: Determinar corretamente os dtype e converters, principalmente de data
def load_file(file_path):
    """Loads the raw file.
    Parameters:
       file_path (str): inform the file path of the raw file to be loaded
    Returns:
       df: a dataframe with the decode data
    """
    df = pd.read_csv(
        file_path,
        encoding='latin',
        dtype='str',
        # dtype=__dtype_dict,
        # converters=__convert_dict,
        # usecols=['TckrSymb', 'Asst', 'XprtnDt', 'OptnTp', 'AllcnRndLot', 'ExrcPric', 'OptnStyle']
        sep=';'
    )
    return df
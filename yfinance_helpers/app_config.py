import logging
import platform
from json import loads
from pathlib import Path
from typing import Union, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


def logging_config(log_file_name: Optional[str] = None,
                   force_local_folder: bool = False,
                   project_name: Optional[str] = None,
                   log_level: int = logging.DEBUG):
    """Create a basic logging file

    Args:
        log_file_name (Optional[str], optional): a file name ending with '.log' which will be stored in the log folder. Defaults to None.
        force_local_folder (bool=False): ignore system parameter and save logs locals within the downloads folder
        project_name (Optional[str]=None): names the logging folder, if ignored, uses the app name
        log_level (int=logging.DEBUG): the log level

    """
    if not project_name:
        project_name = get_project_root_path().name

    # Handles folder to log into
    if force_local_folder:
        logging_folder = Path(get_project_root_path(), project_name, "downloads")
        logging_folder.mkdir(parents=True, exist_ok=True)
    else:
        if platform.system() == 'Linux':
            logging_folder = Path('/var', "log", "my_apps", "python", project_name, )
            logging_folder.mkdir(parents=True, exist_ok=True)
        else:
            logging_folder = Path(get_project_root_path(), project_name, "downloads")
            logging_folder.mkdir(parents=True, exist_ok=True)
    # handles log file name
    if log_file_name:
        logging_file_path = Path(logging_folder, log_file_name)
    else:
        logging_file_path = Path(logging_folder, f'{project_name}.log')

    # Configure the root logger
    logging.basicConfig(
        filename=logging_file_path,  # Global log file name
        level=log_level,  # Global log level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_external_ip_address() -> Union[str, None]:
    """get external ip address"""

    url: str = 'https://jsonip.com/'

    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print("The server couldn't fulfill the request.")
            print('Error code: ', e.code)
        return None

    # read JSOn data
    # https://stackoverflow.com/questions/32795460/loading-json-object-in-python-using-urllib-request-and-json-modules
    encoding = response.info().get_content_charset('utf-8')
    data = response.read()
    json_data = loads(data.decode(encoding))
    return json_data['ip']


def get_project_root_path() -> Path:
    # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
    root_dir = Path(__file__).resolve().parent.parent
    return root_dir


def get_project_download_path() -> str:
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    download_folder_path = Path(get_project_root_path(), "yfinance_helpers", "downloads")
    if not download_folder_path.exists():
        download_folder_path.mkdir(parents=True)
    return str(download_folder_path)


if __name__ == '__main__':
    # print(get_hp_website_visitors_file_path())

    print(get_external_ip_address())

    print(get_project_root_path())

    print(get_project_download_path())

import requests
from bs4 import BeautifulSoup
import os.path


def get_version():
    v = requests.get('https://github.com/NearBirdEZ/Pull_master_naumen/blob/master/source/version')
    soup = BeautifulSoup(v.text, 'html.parser')
    version_online = float(soup.find('td', class_='blob-code blob-code-inner js-file-line').get_text())
    with open(os.getcwd() + '\\version', 'r') as file_with_version:
        local_version = float(file_with_version.readline())
        """
        Перезапись версии в файле. Не актуально - перезапись целой папки.
        file_with_version.truncate(0)
        file_with_version.seek(0)
        file_with_version.write(str(version_online))"""

    return not local_version == version_online

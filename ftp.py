import json
import pprint
import os
import zipfile
import xmltodict
import xml.etree.ElementTree as ET

from ftplib import FTP

DATE_TO_SEARCH = "20221227"

def process_out_dir(file_sys):
    directory = {}
    folders = ftp.nlst("out")
    folders_with_numbers = [folder.split("/")[-1] for folder in folders if len(folder.split("/")[-1]) == 10]
    for folder in folders_with_numbers:
        directory[folder] = None
    file_sys["out"] = directory

def process_number_dir(file_sys):
    for folder in file_sys["out"].keys():
        files = ftp.nlst(f"out/{folder}")
        files_current_date = [file.split("/")[-1] for file in files if DATE_TO_SEARCH in file.split("/")[-1]]
        file_sys["out"][folder] = files_current_date

def download_zip_files(file_sys):
    if not os.path.isdir(f"{DATE_TO_SEARCH}_zip_files"):
        os.mkdir(f"{DATE_TO_SEARCH}_zip_files")
    for folder in file_sys["out"].keys():
        ftp.cwd(f"/out/{folder}")
        for zip_file in file_sys["out"][folder]:
            ftp.retrbinary("RETR " + zip_file ,open(f"{DATE_TO_SEARCH}_zip_files/{zip_file}", 'wb').write)

def process_zip_files():
    if not os.path.isdir(f"{DATE_TO_SEARCH}_xml_files"):
        os.mkdir(f"{DATE_TO_SEARCH}_xml_files")
    zip_files = [file for file in os.listdir(f"{DATE_TO_SEARCH}_zip_files")]
    for zip_file in zip_files[60:100]:
        with zipfile.ZipFile(f"{DATE_TO_SEARCH}_zip_files/{zip_file}") as myzip:
            xml_data = myzip.read(zip_file[:-4])
            if len(xml_data) == 0:
                continue
            dict_data = xmltodict.parse(xml_data)
            with open(f"{DATE_TO_SEARCH}_xml_files/{zip_file[:-4]}.json", "w") as f:
                json.dump(dict_data, f)

ftp = FTP('ftp.zakupki.gov.ru')
ftp.login('fz223free','fz223free')

pp = pprint.PrettyPrinter(depth=4)
file_system = {
    "out": None
}

process_out_dir(file_system)
process_number_dir(file_system)
download_zip_files(file_system)
process_zip_files()
# with open(f'{DATE_TO_SEARCH}.json', 'w') as f:
#     json.dump(file_system, f)
# pp.pprint(file_system)

ftp.close()

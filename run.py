import json
import pprint
import zipfile
from ftplib import FTP

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
        files_current_date = [file.split("/")[-1] for file in files if "20221202" in file.split("/")[-1]]
        file_sys["out"][folder] = files_current_date

if __name__ =="__main__":
    ftp = FTP('ftp.zakupki.gov.ru')
    ftp.login('fz223free','fz223free')

    #pp = pprint.PrettyPrinter(depth=4)
    # file_system = {
    #     "out": None
    # }


    # process_out_dir(file_system)
    # process_number_dir(file_system)
    # with open('20221202.json', 'w') as f:
    #     json.dump(file_system, f)
    # pp.pprint(file_system)
    file = "0000000005_contract_20221202_083819_001.xml.zip"
    folder = file.split('_')[0]
    print(folder)
    ftp.cwd(f'out/{folder}')

    ftp.retrbinary("RETR " + file ,open("from_ftp.zip", 'wb').write)
    with zipfile.ZipFile("from_ftp.zip", 'r') as zip_ref:
        zip_ref.extractall("./resource")
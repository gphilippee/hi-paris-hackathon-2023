"""
Download zip file from https://partage.imt.fr/index.php/s/pqBR9TnSe3tPsHi/download/data.zip and save all files in a folder
"""
import urllib.request
import zipfile
import os


def download_data():
    url = "https://partage.imt.fr/index.php/s/pqBR9TnSe3tPsHi/download/data.zip"
    filehandle, _ = urllib.request.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, "r")
    zip_file_object.extractall()
    zip_file_object.close()
    os.remove(filehandle)


if __name__ == "__main__":
    download_data()

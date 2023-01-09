#! /usr/bin/python3
import os
import re
import requests
import subprocess
import sys
import tempfile
import time
import shutil
import zipfile
import random
import py7zr
import rarfile

# input a link and download the file with a randomly generated name 
def download_file(url):
    local_filename = str(random.randint(100,2555)) + '.tmp'
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

#extract the downloaded file if it is a 7z, rar, or zip file. return the directory of the extracted file. delete the original file
def extract_file(archive_file, destination_dir):
    if zipfile.is_zipfile(archive_file):
        with zipfile.ZipFile(archive_file, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
        return destination_dir
    elif zipfile.is_rarfile(archive_file):
        with rarfile.RarFile(archive_file, 'r') as rar_ref:
            rar_ref.extractall(destination_dir)
        return destination_dir
    elif zipfile.is_7zfile(archive_file):
        with py7zr.SevenZipFile(archive_file, mode='r') as seven_ref:
            seven_ref.extractall(destination_dir)
        return destination_dir
    else:
        raise ValueError('Archive type not supported')
    
#flatten the resulting directory to have only one level, creating a directory if necessary
def flatten_directory(directory):
    for root, dirs, files in os.walk(directory):
        if len(dirs) == 1:
            subdir = os.path.join(root, dirs[0])
            for subroot, subdirs, subfiles in os.walk(subdir):
                for subfile in subfiles:
                    os.rename(os.path.join(subroot, subfile), os.path.join(root, subfile))
            os.rmdir(subdir)

# prompt the user for a name for the resulting directory and rename the directory to that name
def get_new_name(directory):
    new_name = input('Enter new name for ' + directory + ': ')
    if new_name == '':
        new_name = directory
    return new_name

def main():
    url = input('Enter URL: ')
    filename = download_file(url)
    dir_tmp = 'tmp_dir.' + str(random.randint(100,2555))
    extract_file(filename,dir_tmp)
    os.remove(filename)
    directory = dir_tmp
    flatten_directory(directory)
    new_name = get_new_name(directory)
    os.rename(directory, new_name)
    # by default move it to the user skins folder
    move_dir = os.path.abspath('E:\\Steam\\steamapps\\common\\War Thunder\\UserSkins')
    # ask for the model to create a subfolder in the userskins folder
    int_dir = input('Which Model is this skin for?')
    # move_dir is user_skins folder/model/new_dir
    move_dir = os.path.join(move_dir,int_dir,new_name)
    # move the files
    shutil.move(os.path.abspath(new_name), move_dir)
    
if __name__ == '__main__':
    main()

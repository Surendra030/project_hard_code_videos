import os
import subprocess
from mega import Mega
import re
import traceback
from get_mega_instance import fetch_m




def uplox_all_videos(filename,m,f_h):
    m.upload(filename,f_h)

def upload_mkv_files(filename):

    m = fetch_m()  

    folder_name = 'temp_folder'
    file = m.create_folder(folder_name)
    f_h = file[folder_name]
    lst = []

    if os.path.exists(filename):
        uplox_all_videos(filename,m,f_h)
        if '_hardcoded.mp4' not in filename:
            os.remove(filename)
            print(f"Removed file : ",filename)

    print("All files are uploaded sucessfully..")

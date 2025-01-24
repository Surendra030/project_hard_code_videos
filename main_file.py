from mega import Mega
import os
import json
import time
import traceback
import sys
import shutil

from upload_before_coded import upload_mkv_files
from download_video import start_downloading
from get_meta_data import meta_data_main
from hardcode_videos import hardcode_all_videos
from upload_videos import upload_hardcoded_videos_folders
from split_video import split_video_main
from download_mega_all import download_videos
from get_mega_instance import fetch_m
from decrypt import decrypt_json



# Provide the correct file path (relative or absolute)
file_name = "main_sorted_data.json"

def clean_up_files(original_files, not_required_path=os.getcwd()):
    # Get the list of files and folders in the not_required directory
    not_required_files = os.listdir(not_required_path)

    # Convert original_files to a set for faster lookup
    original_files_set = set(original_files)

    # Iterate over the files and folders in the not_required directory
    for item in not_required_files:
        item_path = os.path.join(not_required_path, item)

        # Check if the item is not in the original_files
        if item not in original_files_set:
            # Remove the item (file or folder) if it's not in the original_files
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Remove the file
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the folder
                print(f"Deleted folder: {item_path}")

    # Additionally, iterate over the original_files and check if they exist in not_required
    for item in original_files:
        item_path = os.path.join(not_required_path, item)

        # If the item from original_files is not in not_required, delete it from the filesystem
        if not os.path.exists(item_path):
            if os.path.isfile(item) or os.path.islink(item):
                os.remove(item)  # Remove the file
                print(f"Deleted original file not in not_required: {item}")
            elif os.path.isdir(item):
                shutil.rmtree(item)  # Remove the folder
                print(f"Deleted original folder not in not_required: {item}")



def upload_links_json():

    m = fetch_m()

    files_lst = []

    all_files = m.get_files().items()

    for key, snippet in all_files:
        file_name = snippet["a"]["n"]
        if ".zip" in file_name:
            link = m.export(file_name)
            files_lst.append(link)

    json_file = "videos_links.json"
    with open(json_file, "w") as f:
        json.dump(files_lst, f, indent=4)
    try:

        m.upload(json_file)
    except Exception as e:
        print("Error : ", e)




# Check if the file exists before proceeding
if os.path.exists(file_name):
    keyasjson = os.getenv("PASSWORD")
    json_data = decrypt_json('encrypted_data.json',keyasjson)
    
    aindex = os.getenv("START")
    aindex = int(aindex)
    
    index_num = aindex
    with open(file_name, encoding="utf-8") as f:
        data = json.load(f)

    names_size_lst = {}
    already_files_present = True
    folder_name_lst = []

    if len(data) > aindex:
        obj = [obj for obj in data if obj['sno'] == int(aindex)]
        obj = obj[0] if len(obj) >0 else None
        try:
            
            
            try:
                print(f"{30 * '-'}\n stage : 1")
                print(f"{30 * '^'}")

                print("Starting downloading process...")
                start_time = time.time()    
                start_downloading(obj,json_data)
                elapsed_time = time.time() - start_time
                print(f"Downloading completed successfully. Time taken: {elapsed_time:.2f} seconds.")
            except Exception as e:
                traceback.print_exc()
                print(f"Error during downloading: {e}")

# -----------------at this point all video files are donaloded in local directory -------------
            
            original_files = os.listdir()
            
            for zipfile_name in original_files:
                if '.zip' in  zipfile_name:
                    os.remove(zipfile_name)
            
            original_files = os.listdir()
            print(f"{30*"-"}\n{original_files}\n{30*"-"}")
            
            for video_file in  [file for file in os.listdir() if file.endswith(('.mkv'))]t:
                
  [:6]             temp_video_file = str(video_file)
                print(f"{4*'\t'} -> {video_file}\n\n")
                try:
                    print(f"{30 * '-'}\n stage : 2")
                    print(f"{30 * '^'}")

                    print("Starting metadata extraction process...")
                    start_time = time.time()
                    if os.path.exists(video_file):
                        
                    
                        video_file = meta_data_main(video_file)
                        elapsed_time = time.time() - start_time
                        print(f"Metadata extraction completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error during metadata extraction: {e}")
                    
                try:
                    
                    print(f"{30 * '-'}\n stage : 3")
                    print(f"{30 * '^'}")

                    print("Starting video hardcoding process...")
                    start_time = time.time()
                        
                    
                    if os.path.exists(video_file):
                      
                        video_file = hardcode_all_videos(video_file)
                        elapsed_time = time.time() - start_time
                        print(f"Video hardcoding process completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                    
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error during video hardcoding process: {e}")
                
                
                try:
                    print(f"{30 * '-'}\n stage : 4")
                    print(f"{30 * '^'}")

                    print("Starting upload of MKV files...")
                    start_time = time.time()
                    if os.path.exists(video_file):
                        
                    
                        upload_mkv_files(video_file)
                        elapsed_time = time.time() - start_time
                        print(f"MKV file upload completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error during MKV file upload: {e}")

                try:
                    print(f"{30 * '-'}\n stage : 5")
                    print(f"{30 * '^'}")

                    print("Starting video splitting process...")
                    start_time = time.time()
                    hardcoded__lst = [f for f in os.listdir() if '_hardcoded.mp4' in f]
                    
                    if hardcoded__lst and len(hardcoded__lst)>0:
                        hardcoded_file = hardcoded__lst[0]
                    
                    if os.path.exists(hardcoded_file):
                        
                        
                        zip_file = split_video_main(hardcoded_file)
                        elapsed_time = time.time() - start_time
                        print(f"Video splitting process completed. Processed folders: {folder_name_lst}. Time taken: {elapsed_time:.2f} seconds.")
                    
                    else:
                        print(f" {30*'^'}\n{os.listdir()}\n\n _hardcoded.mp4 file not found...\n")
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error during video splitting process: {e}")
                
                try:
                    
                    print(f"{30 * '-'}\n stage : 6")
                    print(f"{30 * '^'}")

                    print("Starting upload of hardcoded video folders...")
                    
                    start_time = time.time()
                    
                    zipf = [f for f in os.listdir() if '.zip' in f]
                    
                    if zipf and  len(zipf) > 0:
                        zipf = zipf[0]
                            
                        if os.path.exists(zipf):
                            
                            upload_hardcoded_videos_folders(zipf)
                            elapsed_time = time.time() - start_time
                            print(f"Hardcoded video folders uploaded successfully. Time taken: {elapsed_time:.2f} seconds.")
                    else:
                        print("No zip file found..")
                        
                        
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error during upload of hardcoded video folders: {e}")
                
                temp_ass_files = [file for file in os.listdir() if '.ass' in file]
                temp_srt_files = [file for file in os.listdir() if '.srt' in file]
                temp_hardcoded_files = [file for file in os.listdir() if 'hardcoded' in file]
                temp_zip_files = [file for file in os.listdir() if '.zip' in file]
                
                if os.path.exists(temp_video_file):
                    os.remove(temp_video_file)
                
                for f in temp_ass_files:
                    if os.path.exists(f):
                        os.remove(f) 
                for f in temp_srt_files:
                    if os.path.exists(f):
                        os.remove(f) 
                for f in temp_hardcoded_files:
                    if os.path.exists(f):
                        os.remove(f)
                        
                for f in temp_zip_files:
                    if os.path.exists(f):
                        os.remove(f)                
                
                original_files = os.listdir()
                print(f"{30*"-"}\n{original_files}\n{30*"-"}")
                

        
        except Exception as e:
            print("error in line 61 :",e)
            
    else:
        print("No data to process in the decrypted file.")


else:
    print(f"Error: File '{file_name}' not found.")

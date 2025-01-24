from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import os
import time
import json

def check_folder_validity(service, folder_id):
    """Check if the folder ID is valid and accessible."""
    try:
        folder_metadata = service.files().get(fileId=folder_id, fields="id, name").execute()
        print(f"Folder is valid: ")
        return True
    except HttpError as error:
        if error.resp.status in [403, 404]:
            print("Error: Invalid folder ID or insufficient permissions.")
        else:
            print(f"Unexpected error: {error}")
        return False

def list_files_in_folder(service, folder_id):
    """List all files in a specific Google Drive folder."""
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])
    except HttpError as error:
        print(f"Error listing files: {error}")
        return []

def download_file(index,service, file_id, file_name, download_path):
    """Download a file from Google Drive."""
    file_path = os.path.join(download_path, file_name)
    if os.path.exists(file_path):
        print(f"File already exists: {file_name}, skipping download.")
        return
    
    try:
        request = service.files().get_media(fileId=file_id)
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Downloading {index} {int(status.progress() * 100)}%")
        print(f"Downloaded file: {file_name}")
    except HttpError as error:
        print(f"Error downloading {file_name}: {error}")




def start_downloading(obj,data):

    url = obj['driver_Url']
    id = str(url).split("/folders/")[-1]
    
    if 'usp'  in id :
        id = id.split("?usp")[0]
    print("Id : ",id)
    # Path to your service account credentials JSON file
    SERVICE_ACCOUNT_FILE = 'encrypted_data1.json'
    with open(SERVICE_ACCOUNT_FILE,'w',encoding='utf-8')as f:
        json.dump(data,f,indent=4)

    # Scopes required for Google Drive API
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate and build the service
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # Folder ID from the shared folder URL
    FOLDER_ID = id

    # Create a folder to save the downloaded files
    DOWNLOAD_PATH = os.getcwd()
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    # Validate the folder ID
    if not check_folder_validity(service, FOLDER_ID):
        print("Exiting: Folder ID is not valid or inaccessible.")
        exit()

    # Get the list of files in the folder
    files = list_files_in_folder(service, FOLDER_ID)
    if not files:
        print("No files found in the folder or insufficient permissions.")
        exit()

    print(f"Found {len(files)} files in the folder.")

    # Download each file
    for index,file in enumerate(files):
        print(f"Downloading file: {file['name']}")
        download_file(index,service, file['id'], file['name'], DOWNLOAD_PATH)

    print("All files downloaded.")

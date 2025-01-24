import os
import subprocess
from mega import Mega



def fetch_m():
        

    keys = os.getenv("M_TOKEN",'afg154008@gmail.com_megaMac02335!')
    keys = keys.split("_")
    mega  = Mega()
    m = mega.login(keys[0],keys[1])
    return m
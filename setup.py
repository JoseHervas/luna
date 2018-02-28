import os

wd = os.path.abspath(__file__)

folder_list = [
wd+"\\exports\\user_data",
wd+"\\exports\\user_data\\temp",
wd+"\\logs"
]

for folder in folder_list:
    try:
        os.stat(folder)
    except:
        os.mkdir(folder) 

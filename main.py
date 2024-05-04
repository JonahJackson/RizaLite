import os
from os.path import splitext, exists, join
import shutil
from time import sleep
import getpass

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import tkinter as tk
from tkinter import filedialog
import re

import json

# ! FILL IN BELOW
# get input and source and make a tkinter window

# source_dir = ""
# def setDir():
#     SRC = filedialog.askdirectory()
#     source_dir = re.sub('/', '\\'.__repr__(), SRC)
#     print(source_dir)
#     root.quit()



# root = tk.Tk()
# root.title("Riza File Manager")

# SourceText = tk.Label(root, text="Source Folder:").pack()
# SRC = tk.StringVar()

# btn = tk.Button(root, text="Select Folder", command=setDir).pack()



# tk.mainloop()



# ? folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"

source_dir = "C:\\Users\\"+ getpass.getuser() +"\\Downloads"
if not os.path.exists("C:\\Users\\"+ getpass.getuser() +"\\Music\\SFX"):
    os.makedirs("C:\\Users\\"+ getpass.getuser() +"\\Music\\SFX")
dest_dir_sfx = "C:\\Users\\"+ getpass.getuser() +"\\Music\\SFX"
dest_dir_music = "C:\\Users\\"+ getpass.getuser() +"\\Music"
dest_dir_video = "C:\\Users\\"+ getpass.getuser() +"\\Videos"
dest_dir_image = "C:\\Users\\"+ getpass.getuser() +"\\Pictures"
dest_dir_documents = "C:\\Users\\"+ getpass.getuser() +"\\Documents"
if not os.path.exists("C:\\Users\\"+ getpass.getuser() +"\\Documents\\EXE"):
    os.makedirs("C:\\Users\\"+ getpass.getuser() +"\\Documents\\EXE")
dest_exe_documents = "C:\\Users\\"+ getpass.getuser() +"\\Documents\\EXE"
if not os.path.exists("C:\\Users\\"+ getpass.getuser() +"\\Documents\\Code"):
    os.makedirs("C:\\Users\\"+ getpass.getuser() +"\\Documents\\Code")
dest_code_documents = "C:\\Users\\"+ getpass.getuser() +"\\Documents\\Code"


    
def JsonToExtentionList(Json): # * Makes a list of strings from an input json file
    file = open(f"{Json}")
    data = json.load(file)
    extentions_temp = []
    
    for d in data:
        extentions_temp.append(d.get("extensions"))
    extentions_txt = open("extentions.txt", "a")
    extentions_txt.write(str(extentions_temp).replace("[", "").replace("]", ""))
        
    extentions_txt = open("extentions.txt", "r")
    extentions = "extentions = [" + str(extentions_txt.read()).replace("[", "").replace("]", "") + "]"
    exec(extentions)
    extentions_txt.close()
    os.remove("extentions.txt")
    file.close()

    return extentions


# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
exe_extentions = [".exe", ".msi"]
code_extensions = JsonToExtentionList("programming_languages_extentions.json")




def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = str(join(dest, name))
        newName = str(join(dest, unique_name))
        os.rename(oldName, newName)
    shutil.move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_exe_files(entry, name)
                self.check_code_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")
    def check_exe_files(self, entry, name): # * Checks all EXE Files
        for exe_extention in exe_extentions:
            if name.endswith(exe_extention) or name.endswith(exe_extention.upper()):
                move_file(dest_exe_documents, entry, name)
                logging.info(f"Moved executable file: {name}")
    def check_code_files(self, entry, name): # * Checks all Code Files
        for code_extension in code_extensions:
            if name.endswith(code_extension) or name.endswith(code_extension.upper()):
                move_file(dest_code_documents, entry, name)
                logging.info(f"Moved code file: {name}")


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
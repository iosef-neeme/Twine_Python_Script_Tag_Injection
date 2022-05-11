__version__ = '0.2.0'

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import webbrowser
import os
import json

script_source = ""
project_directory = ""
mode = ""

"""
    This function takes the path to the file and injects a string, at a certain line, in the file.
    The variable index indicates the line were your string will be injected-1.
    The variable "value" holds the string that will be injected in the html file.
"""
def Get_Script_Files():
    global script_source
    global project_directory
    global mode
    while True: 
        try:
            files = os.listdir(f"{project_directory}/{mode}")
            break
        except:
            print(f"Could not find the directory {mode} specified in the json file.\
                    \n Would you like me to create the directories according to the default configuration?")
            answer = input()
            if(answer == "yes"):
                if not os.path.exists(f"{project_directory}/dev"):
                    os.mkdir(f"{project_directory}/dev")
                if not os.path.exists(f"{project_directory}/tmp"):
                    os.mkdir(f"{project_directory}/tmp")
                if not os.path.exists(f"{project_directory}/pub"):
                    os.mkdir(f"{project_directory}/pub")
                continue
            else:
                exit(0)
    js_script_pefix = f"<script id='my_script' type='text/javascript' src='{project_directory}/{mode}/"
    cs_script_pefix = f"<script id='stylesheet' type='text/javascript' src='{project_directory}/{mode}/"
    script_sufix = "'></script>\n"
    for i in files:
        if ".js" in i or ".mjs" in i:
            script_source += js_script_pefix + i + script_sufix
        if ".css" in i:
            script_source += cs_script_pefix + i + script_sufix

"""
    This function read the execution mode and stores the value in a global variable called mode.
"""
def Read_Execution_Mode():
    global project_directory 
    global mode
    print("Please indicate the project directory")
    project_directory = input()
    print("Type 'dev' for development mode.\nType 'pub' publish mode.\nType 'q' to exit the program.")
    mode = input()
    while True:
        Get_Script_Files()
        if(mode.lower() == "dev"):
            return "tmp"
        if(mode == "pub"):
            return project_directory
        if(mode == "q"):
            exit()
        print("Type 'dev' for development mode.\nType 'development' for development mode.\nType 'q' to exit the program.")
        mode = input()

"""
    This function takes the path to the file and injects a string, at a certain line, in the file.
    The variable index indicates the line-1 where your string will be injected.
    The variable "value" holds the string that will be injected in the html file.
"""
def Insert_script(path):
    index = 6
    value = script_source
    print(path)
    with open(path, "r") as f:
            cuvinte = f.readlines(-1)
    cuvinte.insert(index, value)
    cuvinte = "".join(cuvinte)
    time.sleep(0.01)
    with open(path, "w") as f:
        f.write(cuvinte)

"""
    This function create a copy of the file that was created by the Twine IDE.
"""
def Make_file_copy(original_path):
    global project_directory
    destination_path = f"{project_directory}/tmp/1.html"
    os.popen(f'cp {original_path} {project_directory}/tmp/1.html')
    Insert_script(destination_path)
    webbrowser.open('file://' + destination_path)

"""
    This is the function that will be used as handler for the event on_create which will be triggered when a file is created in the overseen directory aka folder.
    It checks if the new file is an html file and if it is, assumes it is the file that was just created by twine, calles for Insert_script function and reopens the file in a new tab.
"""
def on_created(event):
    path = event.src_path
    time.sleep(0.8)
    if os.path.isfile(path):
        if path.endswith("html"):
            print(f"hey, {path} has been created! ")
            Make_file_copy(path)

"""
    This is the main function.
"""
def main():

    path = Read_Execution_Mode()
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive = go_recursively)

    my_observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

if __name__ == "__main__":
    main()
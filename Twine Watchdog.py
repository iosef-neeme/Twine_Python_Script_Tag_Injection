__version__ = '0.1.0'

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import webbrowser
import os


def Read_Execution_Mode():
    print("Type 'test' for test mode.\nType 'normal' for normal mode.\nType publish.\nType 'q' to exit the program.")
    mode = input()
    script_pefix = "<script id='my_script' type='text/javascript' src='"
    script_sufix = "'></script>\n"
    while True:
        if(mode == "publish"):
            script_source = script_pefix+"*** Put here the path to the script, for publishing mode"+script_sufix
            return "pub"
        if(mode == "test"):
            script_source = script_pefix+"*** Put here the path to the script, testing mode"+script_sufix
            return "tmp"
        if(mode == "normal"):
            script_source = script_pefix+"*** Put Here your path to the script, for normal mode"+script_sufix
            return "tmp"
        if(mode == "q"):
            exit()
        print("Type 'test' for test mode.\nType 'normal' for normal mode.\nType 'q' to exit the program.")
        mode = input()


"""
    This function takes the path to the file and injects a string, at a certain line, in the file.
    The variable index indicates the line were your string will be injected-1.
    The variable "value" holds the string that will be injected in the html file.
"""
def Insert_script(path):
    index = 6
    value = script_source
    value += "<link rel='stylesheet' href='*** Put here the source of the script you want to be added'>\n"
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
def Make_file_copy(path):
    original_path = path
    target_path = "Put here your path to the place you want to save the file"
    os.popen(f'cp {original_path} {target_path}')
    path = target_path
    #return path
    Insert_script(path)
    webbrowser.open('file://' + path)

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
            #path = Make_file_copy(path)
            #Insert_script(path)
            #webbrowser.open('file://' + path)
            Make_file_copy(path)

"""
    This is the main function.
    Here is 
"""
script_source = ""  
def main(mode):
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    if(mode == "tmp"):
        path = "/tmp/"
    else:
        path = "Put here the path for the folder where you want to get you "
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

if __name__ == "__main__":
    main(Read_Execution_Mode())
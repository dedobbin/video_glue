import os
import time
import ffmpeg
from pathlib import Path
import shutil
import os
from datetime import datetime
import glob


def create_dir(path):
    if os.path.exists(path) and not os.path.isdir(path):
        print(f"{path} already exists and is not a dir.. aborting")
        return False
    
    if not os.path.isdir(path):
        os.mkdir(path)
    return True

def create_stitch_list_file(path):
    with open(path,'w') as f:
        print(f"Created empty stitch list at {os.path.abspath(path)}")

def build_stitch_list(should_stop, incoming_dir):
    stitch_list = []
    print("Build stitch list")
    while True:
        if should_stop():
            print("Got stop signal, will return stitch list")
            return stitch_list
        
        #print(f"Files in incoming dir: ", len(os.listdir(incoming_dir)))
        for incoming_file in os.listdir(incoming_dir):
            file_path = incoming_dir+incoming_file           
            if file_path in stitch_list:
                continue
            print("Inserted in stitch list ", file_path)
            stitch_list.append(file_path)
        time.sleep(5)

def stitch(should_stop, incoming_dir="incoming/", output_dir="output/"):
    resulting_filepath = f"{output_dir}output_{datetime.timestamp(datetime.now())}.mp4"

    create_dir(incoming_dir)
    create_dir(output_dir)

    stitch_file_path = "stitch_list.txt"
    create_stitch_list_file(stitch_file_path)


    print("Start building stitch list")
    stitch_list = build_stitch_list(should_stop, incoming_dir)
    
    print("Got end signal, will glue")
    
    if len(stitch_list) > 0:
        with open(stitch_file_path, 'w') as f:
            for file_path in stitch_list:
                f.write(f"file '{file_path}'\n")
        ffmpeg.input(stitch_file_path, f='concat', safe=0).output(resulting_filepath, codec='copy', loglevel='quiet').overwrite_output().run()
    if not os.path.exists(resulting_filepath) or not os.path.isfile(resulting_filepath):
        return False

    # cleanup to prepare for next round
    create_stitch_list_file(stitch_file_path)
    files = glob.glob(incoming_dir + "*")
    for f in files:
        os.remove(f)

    print ("Successfully created " + resulting_filepath)
    return resulting_filepath


if __name__ == "__main__":
    stitch(lambda : False, "incoming/", "output/")
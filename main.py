import os
import time
import ffmpeg
from pathlib import Path
import shutil
from random import randrange

def should_stop():
    return False
    #return randrange(0,20)==0

def create_dir(path):
    if os.path.exists(path) and not os.path.isdir(path):
        print(f"{path} already exists and is not a dir.. aborting")
        return False
    
    if not os.path.isdir(path):
        os.mkdir(path)
    return True

def stitch(should_stop, incoming_dir="incoming/", output_dir="output/", processed_dir="processed/"):
    create_dir(incoming_dir)
    create_dir(output_dir)
    create_dir(incoming_dir)
    
    output_file = f"output_{time.time()}.mp4"
    stitch_file_path = "stitch_list.txt"

    with open(stitch_file_path, 'w') as f:
        f.write(f"file '{output_dir+output_file}'\n")
    
    while(True):
        if should_stop():
            break
        for incoming_file in os.listdir(incoming_dir):
            if incoming_file not in os.listdir(processed_dir):
                print(f"Found unprocessed file {incoming_file}")
                if not os.path.exists(output_dir+output_file):
                    print(f"{incoming_file} is first, copy to output directly")
                    shutil.copy(incoming_dir+incoming_file, output_dir+output_file)
                else:
                    with open(stitch_file_path, 'a') as f:
                        f.write(f"file '{incoming_dir+incoming_file}'")
                    
                    with open(stitch_file_path, 'r') as f:
                        print(f"stitching:\n{f.read()}")
                    ffmpeg.input(stitch_file_path, f='concat', safe=0).output(output_dir+"tmp.mp4", codec='copy').overwrite_output().run()
                    Path(output_dir+"tmp.mp4").rename(output_dir+output_file) #move
                    
                    with open(stitch_file_path, "w+") as f:
                        lines = f.readlines()
                        f.write("\n".join(lines[:-1]))

                print(f"moving {incoming_file} to {processed_dir}")
                Path(incoming_dir+incoming_file).rename(processed_dir+incoming_file) #move
            else:
                print(f"{incoming_file} is already processed")
        
        time.sleep(5)

def main():
    while True:
        print("Start stitching")
        stitch(should_stop)
        print("End stitching")

if __name__ == "__main__":
    main()
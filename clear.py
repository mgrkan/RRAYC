from conf import SAMPLE_OUTPUTS, SAMPLE_INPUTS, BASE_DIR, VIDEOS_DIR
import shutil
import os
import pathlib
import sys
from mail_notifier import sendMail
import video_creator

def folder_preparation():
    shutil.rmtree(SAMPLE_OUTPUTS, ignore_errors=True)
    print("erased folder outputs")     #ERASES ALL OF THE OLD POST OR COMMENT VIDEOS TO WRITE NEW ONES
    os.mkdir(SAMPLE_OUTPUTS)           #CREATES EMPTY OUTPUT FOLDER
    print("created folder outputs")
    shutil.copyfile(pathlib.Path(BASE_DIR + "/outro.mp4"),      #COPIES OUTRO TO OUTPUTS IN ORDER TO ADD THE OUTRO WHEN ADDING ALL OUTPUTS TOGETHER
                    pathlib.Path(SAMPLE_OUTPUTS + "/outro.mp4"))
    print("copied outro to outputs")
    shutil.rmtree(pathlib.Path(SAMPLE_INPUTS + "/imgs"), ignore_errors=True)  #ERASES ALL THE COMMENT OR POST IMAGES THAT WERE ALREADY USED
    print("erased folder imgs")
    os.mkdir(pathlib.Path(SAMPLE_INPUTS + "/imgs"))
    print("created folder imgs")
    shutil.rmtree(pathlib.Path(SAMPLE_INPUTS + "/audio"), ignore_errors=True)
    print("erased folder audio")
    os.mkdir(pathlib.Path(SAMPLE_INPUTS + "/audio"))
    print("created folder audio")
    shutil.rmtree(pathlib.Path(VIDEOS_DIR + "/new_vids"), ignore_errors=True)
    print("erased new videos folder")
    os.mkdir(pathlib.Path(VIDEOS_DIR + "/new_vids"))
    print("created new_vids folder")

def mid_folder_preparation():
    shutil.rmtree(SAMPLE_OUTPUTS, ignore_errors=True)
    print("erased folder outputs")     #ERASES ALL OF THE OLD POST OR COMMENT VIDEOS TO WRITE NEW ONES
    os.mkdir(SAMPLE_OUTPUTS)           #CREATES EMPTY OUTPUT FOLDER
    print("created folder outputs")
    shutil.copyfile(pathlib.Path(BASE_DIR + "/outro.mp4"),      #COPIES OUTRO TO OUTPUTS IN ORDER TO ADD THE OUTRO WHEN ADDING ALL OUTPUTS TOGETHER
                    pathlib.Path(SAMPLE_OUTPUTS + "/outro.mp4"))
    print("copied outro to outputs")
    shutil.rmtree(pathlib.Path(SAMPLE_INPUTS + "/imgs"), ignore_errors=True)  #ERASES ALL THE COMMENT OR POST IMAGES THAT WERE ALREADY USED
    print("erased folder imgs")
    os.mkdir(pathlib.Path(SAMPLE_INPUTS + "/imgs"))
    print("created folder imgs")
    shutil.rmtree(pathlib.Path(SAMPLE_INPUTS + "/audio"), ignore_errors=True)
    print("erased folder audio")
    os.mkdir(pathlib.Path(SAMPLE_INPUTS + "/audio"))
    print("created folder audio")
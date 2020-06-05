"""

ADB command for YouTube and Browsing
Let us see how we can automate the YouTube and browsing

1. Launching YouTube and play video

To do so we have to fire below adb shell command

"adb shell am start  https://www.youtube.com/watch?v=6bGdIAf2J_k"

here am start will start the YouTube app and will pass the url v=6bGdIAf2J_k the video path.

2. Launching YouTube in Chrome Browser

To launch the YouTube in chrome browser you have to fire the below adb command

"adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main "https://youtu.be/6bGdIAf2J_k"

2. Launch Browser and go to your favourite websites

To launch the browser there are two different ways

"adb shell input keyevent 64
adb shell input text "https://mobile-automation-testing.blogspot.com" && adb shell input keyevent 66"

Here KeyEvent 64 for launching the browser
         KeyEvent 66 stands for 66 -> KEYCODE_ENTER

The other way to launch the browser is as below

"adb shell am start -a android.intent.action.VIEW -d http://https://mobile-automation-testing.blogspot.com"
In this you can directly pass the url.

3. Launch Browser and download data

Below is the command used for launching the browser and downloading the online

"adb shell am start -a android.intent.action.VIEW -d https://speed.hetzner.de/10GB.bin"

4. Launch Browser and play Music online

Below is the command for launching the browser and playing the music online

"adb shell am start -a android.intent.action.VIEW -d http://stream-tx3.radioparadise.com/mp3-192"


"""

import os
import signal
import sys
import time
from time import sleep
import datetime
import warnings
import pprint
import logging
import subprocess
import threading
from PIL import Image
import re
import shutil
from Android.call_sms_mms import *


class Single_UE_Scenarios():
    """
    Check the mobile data and then stream videos in youtube
    """
    def __init__(self):
        #check if mobile is up, bring up the mobile
        print("********Single UE Scenarios********")
        pass
    def start_adb_logs(self):
        """Start capturing adb logs"""
        print("start capturing adb logs....")
        file_name = "adblogs_"+time.strftime("%Y-%m-%d-%H-%M-%S")+".txt"
        self.adblog=open(file_name,'w')
        self.adblog.truncate(0)
        self.adb_log_proc = subprocess.Popen("adb logcat",stdout=self.adblog)
        #print(self.adb_log_proc.communicate()[0])

    def signal_handler(self):
        sys.exit(0)

    def stop_adb_logs(self):
        """Stop capturing adb logs"""
        #signal.signal(signal.SIGINT, self.signal_handler)
        self.adb_log_proc.terminate()
        #self.adb_log_proc.wait()
        print("stopped capturing the adb logs...\n")
        self.adblog.close()

    def download_files(self, remote_path_andriod, dest_path):
        #adb pull remote local
        #To copy a file or directory and its sub-directories from the device
        subprocess.Popen(r'adb pull ' + remote_path_andriod + "  " + dest_path, stdout=subprocess.PIPE)

    def upload_files(self):
        #adb push local remote
        #To copy a file or directory and its sub-directories to the device
        subprocess.Popen(r'adb push C:\koti_Learning\Android\adb-commands.pdf /sdcard/', stdout=subprocess.PIPE)


    def get_devices(self):
        #adb devices -l
        #adb -s serial number
        pass


    def _get_device_serial_number(self):
        device = os.popen("adb devices").read().split('\n', 1)
        #print(device)
        if device[1] == '\n':
            print("No Device connected to station.\nConnection of Android device is required...")
            sys.exit(0)
            #print("Waiting for connection...")

        # elif (multi device case):
        #   pass
        else:
            self.ad_serial_number = device[1].split('device')[0]
            print(self.ad_serial_number)
            print("Device with adb id " + self.ad_serial_number + "is connected")
            logs_dir = os.mkdir(time.strftime("%Y-%m-%d-%H-%M-%S"))
            parent_folder = os.getcwd().join(["Output_files_logs", logs_dir])
            print(parent_folder)



    def play_youtube(self):
        """To stream video in youtube"""
        print("staring to play youtube video...")
        start_video_command = str("adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v=mUxS-35qO44")
        #adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v=mUxS-35qO44
        #adb shell am force-stop com.google.android.youtube
        #os.system(start_video_command)
        subprocess.Popen(start_video_command, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        print("youtube is running ...")
        #sleep(60)
        #os.system(stop_video_command)

        #subprocess.Popen(stop_video_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("youtube playing is stopped")
        #start video
        #pause/resume video
        #stop video
        #exit browser/app

    def stop_youtube(self):
        stop_video_command = str("adb shell am force-stop com.google.android.youtube")
        subprocess.Popen(stop_video_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Youtube application is stopped Playing...")

    def scrn_shot(self):
        """Capturing screen in android device"""

        file_name = 'screen_capt_adb_'+time.strftime("%Y-%m-%d-%H-%M-%S")+'.png'
        andriod_file="/sdcard/"+file_name
        dest_folder=os.getcwd()
        scrn_capt=subprocess.Popen('adb shell screencap -p ' + andriod_file, stdout=subprocess.PIPE)
        scrn_capt.wait()
        scrn_capt.terminate()
        print(dest_folder)
        self.download_files(andriod_file, dest_folder)
        sleep(2)
        subprocess.Popen('adb shell rm -rf '+ andriod_file)
        im=Image.open(os.path.join(dest_folder, file_name))
        im.show()
        sleep(2)
        os.system("TASKKILL /F /IM Microsoft.Photos.exe")


    def scrn_recorder(self):
        print("Screen Recording started...")
        file_name = 'screen_rec_adb_'+time.strftime("%Y-%m-%d-%H-%M-%S")+'.mp4'
        andriod_file = "/sdcard/" + file_name
        dest_folder=os.getcwd()
        scrn_rec = subprocess.Popen('adb shell screenrecord --time-limit=120 '+andriod_file, stdout=subprocess.PIPE)
        scrn_rec.wait()
        self.download_files(andriod_file, dest_folder)
        subprocess.Popen('adb shell rm -rf ' + andriod_file)

    def camera_toggle(self):
        front_cam = 1
        back_cam = 0
        command=r"adb shell am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING "
        print("Opening front camera")
        subprocess.Popen(command+str(1),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print("Opening Back Camera")
        subprocess.Popen(command+str(0), stdout=subprocess.PIPE,stderr=subprocess.PIPE)


    def __del__(self):
        pass


def objectCreation():
    stream_obj = Single_UE_Scenarios()
    return stream_obj

if __name__ == "__main__":
    send_sms("4b828e21")
    """
    stream_obj=Single_UE_Scenarios()
    stream_obj._get_device_serial_number()
    stream_obj.start_adb_logs()
    stream_obj.scrn_recorder()
    stream_obj.play_youtube()
    stream_obj.upload_files()
    [stream_obj.scrn_shot() for i in range(10)]
    #[stream_obj.scrn_recorder() for i in range(10)]
    stream_obj.stop_youtube()
    stream_obj.stop_adb_logs()
    """
    #logs_thread=threading.Thread(target=stream_obj.start_adb_logs())
    #youtube_thread=threading.Thread(target=stream_obj.play_youtube())
    #scrn_shot_thread=threading.Thread(target=stream_obj.scrn_shot())
    #scrn_record_thread = threading.Thread(target=stream_obj.scrn_recorder())
    #logs_thread.start()
    #youtube_thread.start()
    #[scrn_shot_thread.start() for i in range(3)]
    #scrn_shot_thread.join()
    #youtube_thread.join()
    #logs_thread.join()
    #voice_call_thread=threading.Thread(target=stream.obj.call())
    #sms_thread = threading.Thread(target=stream.obj.sms())
    # mms_thread = threading.Thread(target=stream.obj.mms())
    # sms_thread = threading.Thread(target=stream.obj.sms())
    #stream_obj.start_adb_logs()
    #stream_obj._get_device_serial_number()
    #stream_obj.play_youtube()
    #stream_obj.scrn_shot()
    #stream_obj.scrn_recorder()
    #stream_obj.stop_adb_logs()
import numpy as np
import os
import cv2
import time
import sys

'''
    File name: timer_generator.py
    Author: Katorin
    Date created: 7th March 2020
    Date last modified: 8th March 2020
    Version: 1.0
    Python Version: 3.7.6
'''

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# get dimension of video
def get_dims(res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

# get type of video to write
def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def get_img(label, width, height):
    # parameter for the image representing the time
    # 3 is indispensable for writing image to video
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    scale = (width * width) / (400 * 400)
    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = int(scale * 1.5)
    color = (255, 255, 255)

    # put label
    (label_width, label_height), baseline = cv2.getTextSize(label, font, scale, thickness)
    cv2.putText(frame, label, ((width - label_width) // 2, (height + label_height) // 2), font, scale, color, thickness, cv2.LINE_AA)

    return frame

def get_total_time_in_second(period: str):
    m, s = period.split(':') # get minute and second
    m, s = int(m), int(s)
    return 60 * m + s

def time_to_string(period: int):
    m, s = period // 60, period % 60
    m, s = str(m), str(s)
    if len(m) == 1:
        m = '0' + m
    if len(s) == 1:
        s = '0' + s
    return m + ':' + s

def get_file_name(period: str):
    m, s = period.split(':') # get minute and second
    filename = str(int(s)) + ' seconds'
    if int(s) == 0:
        filename = ""
    if int(s) == 1:
        filename = filename[0 : len(filename) - 1]
    if int(m) == 0:
        return filename
    if int(m) == 1:
        filename = str(int(m)) + ' minute ' + filename
    else:
        filename = str(int(m)) + ' minutes ' + filename
    if filename[-1] == ' ':
        filename = filename[0 : len(filename) - 1]
    return filename

def get_workload_done(done):
    loading_length = 50
    rem = 100 - done
    done = int(done * loading_length)
    res = '█' * done + '.' * (loading_length - done)
    return '|' + res + '|';

def create_countdown_video(period, fps, resolution):
    filename = 'videos/' + get_file_name(period) + '.avi'
    width, height = get_dims(resolution)

    # tools for writing video
    out = cv2.VideoWriter(filename, get_video_type(filename), fps, (width, height))
    
    # total time and remain time to countdown
    total_time = get_total_time_in_second(period)
    remain_time = total_time
    print('Generating timer video:')
    while remain_time >= 0:

        # work processed
        work = (total_time - remain_time) / total_time
        # if work == 0.75:
        #     print('75%', 'done')
        # elif work == 0.5:
        #     print('50%', 'done')
        # elif work == 0.25:
        #     print('25%', 'done')
        sys.stdout.write('\r    Generating: ' + get_workload_done(work) + ' doing sth!')
        sys.stdout.flush()
        
        # image to write
        img = get_img(time_to_string(remain_time), width, height)

        # write images
        for i in range(fps):
            out.write(img)
        remain_time -= 1

    print('\nHurray, 100%', 'done!!!')
    out.release()
    cv2.destroyAllWindows()

def is_valid_period(period: str):
    if period.count(':') != 1:
        return False
    minute, second = period.split(':')
    try:
        minute = int(minute)
        second = int(second)
        if minute >= 60 or second >= 60:
            return False
        return True
    except:
        return False

if __name__ == "__main__":
    """
    Parameters
    ----------
    period : str
        The time that the timer should be set
    fps : int/float
        frames per second
    resolution : str
        video resolution
    """
    period = "time"
    fps = 1
    resolution = '720p'
    promt = 'How long do you want to set the timer(< 1 hour)? (Please type in "minutes:seconds" format) '
    while not is_valid_period(period):
        period = input(promt)
        promt = "Your input is invalid. Please type again!!! "
    startTime = time.time()
    create_countdown_video(period, fps, resolution)
    print(f"Process {resolution} - {get_file_name(period)} video with {fps} fps in:", time.time() - startTime, 'seconds')



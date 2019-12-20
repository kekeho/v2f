# Copyright (c) 2019 Hiroki Takemura (kekeho)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import cv2
import numpy as np
import os
import datetime


from typing import List


class Frame(object):
    def __init__(self, frame: np.ndarray, index: int, video_filename, time: datetime.datetime):
        self.frame: np.ndarray = frame
        self.frame_index = index
        self.video_filename = video_filename
        self.time: datetime.datetime = time


def split(filename: str, interval=1, fps_info: float = None) -> List[Frame]:
    capture_stream = cv2.VideoCapture(filename)
    video_mtime = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)
    video_fps = fps_info if fps_info else capture_stream.get(cv2.CAP_PROP_FPS)

    print(video_fps)

    if not capture_stream.isOpened():
        return np.ndarray([])

    # Read frames
    buffer = []
    frame_index = 0
    while True:
        is_open, frame = capture_stream.read()
        if not is_open:
            break  # End of file

        if frame_index % interval == 0:
            timedelta = datetime.timedelta(seconds=frame_index / video_fps)
            f = Frame(frame, frame_index, filename, video_mtime + timedelta)
            buffer.append(f)
        
        frame_index += 1
    
    return buffer


def save_frame(frame: Frame) -> None:
    dirname = os.path.dirname(frame.video_filename)
    filename, file_ext = os.path.splitext(os.path.basename(frame.video_filename))
    frame_filename = f'{filename}-{frame.frame_index}.jpg'

    savedir = os.path.join(dirname, filename)
    try:
        os.mkdir(savedir)
    except FileExistsError:
        pass

    print(frame.time)

    cv2.imwrite(os.path.join(savedir, frame_filename), frame.frame)
    os.utime(os.path.join(savedir, frame_filename), (frame.time.timestamp(), frame.time.timestamp()))

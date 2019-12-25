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

    def save(self):
        dirname = os.path.dirname(self.video_filename)
        filename, file_ext = os.path.splitext(
            os.path.basename(self.video_filename))
        frame_filename = f'{filename}-{self.frame_index}.jpg'

        savedir = os.path.join(dirname, filename)
        try:
            os.mkdir(savedir)
        except FileExistsError:
            pass

        cv2.imwrite(os.path.join(savedir, frame_filename), self.frame)
        os.utime(os.path.join(savedir, frame_filename),
                 (self.time.timestamp(), self.time.timestamp()))


def split(filename: str, interval=1, fps_info: float = None) -> None:
    """ Split video & save frames
    Args:
        filename: video filename
        interval: get frames per interval
        fps_info: give fps info (none: get from file header)
    """

    capture_stream = cv2.VideoCapture(filename)
    video_mtime = datetime.datetime.fromtimestamp(os.stat(filename).st_mtime)
    video_fps = fps_info if fps_info else capture_stream.get(cv2.CAP_PROP_FPS)

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
            f.save()
            del f

        del frame
        frame_index += 1

    return buffer

from cv2 import cv2 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from settings import Settings

# 读取视频
def read_video(read_path, write_path, filter):
    cap = cv2.VideoCapture(read_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        # 设置滤波器
        if filter is not None:
            frame = filter(frame)

        print(f'Writing frame: {count}.jpg.....')
        cv2.imwrite(write_path + str(count) + '.jpg',frame)
        
        count += 1 

    cap.release()
    cv2.destroyAllWindows() 

def read_frames(path):
    frames = []
    count = 0
    while True:
        try:
            print(f'Reading frame: {count}.jpg....')
            frames.append(read_frame(count, path))
        except Exception as e:
            print(e)
            return frames
        
        count += 1

    return frames

# 存储视频
def store_video(frames, path):
    height, width, _ = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), 30, size)
    count = 0
    for frame in frames:
        print(f'Appending frame: {count}.jpg....')
        out.write(frame)
        count += 1

    out.release()

# 读取某一帧
def read_frame(index, path):
    image = Image.open(path + f'{index}.jpg')
    return np.array(image)

# 滤波
def filter_frame(frame):
    thresh = 90
    img_binary = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]

    return img_binary

def produce_frames(frames):
    bg = np.array(Image.open('bg.jpg'))
    bg = cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)
    bg_s = np.array(Image.open('bg_s.jpg'))
    bg_s = cv2.cvtColor(bg_s,cv2.COLOR_BGR2RGB)


    frames_generated = []
    for frame in frames:
        res1 = cv2.bitwise_and(frame, bg)
        res2 = cv2.bitwise_and(cv2.bitwise_not(frame), bg_s)
        res = cv2.bitwise_xor(res1, res2)

        frames_generated.append(res)

    return frames_generated

# read_video(Settings.video_origin, Settings.imgs_origin, None)
frames = read_frames(Settings.imgs_origin)
frames_generated = produce_frames(frames)
store_video(frames_generated, Settings.video_generated)


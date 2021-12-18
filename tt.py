import os
import cv2
import gc
from multiprocessing import Process, Manager
import time
from tkinter import *
from PIL import Image,ImageTk

class VideoRecoder(object):
    def __init__(self) -> None:
        super().__init__()


def write(queue, cam, top: int) -> None:
    """
    :param cam: 攝影機編號
    :param stack: Manager.Queue()
    :param top: 緩衝
    :return: None
    """
    print('Process to write: %s' % os.getpid())
    cap = cv2.VideoCapture(cam,cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 15)

    # print(cap.get(cv2.CAP_PROP_EX))
    while True:
        ret = cap.grab()
        if not ret:
            continue
        else:
            ret, img = cap.retrieve()
            exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
            print(f"exposure {cam} : ",exposure)
            if(ret):
                queue.put(img, True, top)

def save(queue, cam_id) -> None:
    print('Process to save: %s' % os.getpid())
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    output_video = cv2.VideoWriter("video//" + str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())) + f"{cam_id}" + '.avi', codec, 30, (640, 480))
    while True:
        frame = queue.get(True) # blocking operation
        output_video.write(frame)
        cv2.imshow(f"cam {cam_id} img", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            output_video.release()
            break

if __name__ == '__main__':
    cam1 = 2
    # cam3 = 3
    cam2 = 1
    q = Manager().Queue()
    q1 = Manager().Queue()
    q2 = Manager().Queue()
    pw = Process(target=write, args=(q, cam1, 100))
    ps = Process(target=save, args=(q, cam1))
    pw1 = Process(target=write, args=(q1, cam2, 100))
    ps1 = Process(target=save, args=(q1, cam2))
    # pw2 = Process(target=write, args=(q2, cam3, 100))
    # ps2 = Process(target=save, args=(q2, cam3))
    
    
    pw.start()
    pw1.start()
    # pw2.start()
    ps.start()
    ps1.start()
    # ps2.start()
    ps.join()
    ps1.join()
    # ps2.join()
    pw.terminate()
    pw1.terminate()
    # pw2.terminate()

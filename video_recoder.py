import cv2
from multiprocessing import  Manager
from threading import Thread
import time
import os


class VideoRecoder(object):
    def __init__(self,cam_list: list) -> None:
        super().__init__()
        self.cam_list = cam_list

    def set_cap(self) -> None:
        self.cap_list = list()
        for i in range(len(self.cam_list)):
            self.cap_list.append(cv2.VideoCapture(self.cam_list[i], cv2.CAP_DSHOW))
            self.cap_list[i].set(cv2.CAP_PROP_FPS, 15)

    def set_queue(self) -> None:
        self.q = list()
        for i in range(len(self.cam_list)):
            self.q.append(Manager().Queue())

    def read_frame(self,top: int) -> None:
        while True:
            for i in range(len(self.cap_list)):
                ret = self.cap_list[i].grab()
                if not ret:
                    continue
                else:
                    ret, img = self.cap_list[i].retrieve()
                    exposure = self.cap_list[i].get(cv2.CAP_PROP_EXPOSURE)
                    print(f"exposure {i} : ", exposure)
                    if (ret):
                        self.q[i].put(img, True, top)

    def start_recording(self) -> None:
        self.read_frame(1)
        self.save_frame()

    def save_frame(self) -> None:
        codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        for i in range(len(self.cam_list)):
            output_video = cv2.VideoWriter(
                "video//" + str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())) + f"{i}" + '.avi', codec, 30,
                (640, 480))
            while True:
                frame = self.q.get(True)
                output_video.write(frame)
                cv2.imshow(f"cam {i} img", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    output_video.release()
                    break

if __name__ == '__main__':
    cam_list = [1,2]
    video_recoder = VideoRecoder(cam_list)
    video_recoder.set_cap()
    video_recoder.set_queue()
    thread1 = Thread(target=video_recoder.read_frame, args=(100,))
    thread1.daemon = True
    thread1.start()
    # video_recoder.start_recording()

    
from threading import Thread, Event
from queue import Queue
import cv2
import time
import os

class VideoRecorder(Thread):
    def __init__(self, cam_list: list):
        Thread.__init__(self)
        self.daemon = True

        self.kill_switch = Event()
        self.frame_queue = Queue()
        self.cap_list = [cv2.VideoCapture(
            id, cv2.CAP_DSHOW) for id in cam_list]
        for cap in self.cap_list:
            cap.set(cv2.CAP_PROP_FPS, 15)

    def run(self):
        while not self.kill_switch.is_set():
            for cap in self.cap_list:
                if not cap.grab():
                    break  # wait until both cam are ready
            else:
                # put frame into queue
                moment = list()
                for idx, cap in enumerate(self.cap_list):
                    ret, frame = cap.retrieve()
                    if not ret:
                        print(f"cam{idx} retrieve failed")
                        break
                    moment.append(frame)
                else:
                    self.frame_queue.put(moment, True)

    def __write_frames(self):
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        video_streams = [cv2.VideoWriter(
            f"video//{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}_{i}.avi",
            codec, 15, (640, 480))
            for i in range(len(self.cap_list))]
        write_count = [0] * len(self.cap_list)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                for stream in video_streams:
                    stream.release()
                self.kill_switch.set()
                print(f"{write_count}")
                return  # leave
            moment = self.frame_queue.get(True)
            for pos in range(len(moment)):
                video_streams[pos].write(moment[pos])
                cv2.imshow(f"cam{pos}", moment[pos])
                write_count[pos] += 1

    @classmethod
    def start_recording(cls, cams: list):
        """
            Start capture thread and keep writting frames to disk
        """
        t = cls(cams)
        t.start()
        t.__write_frames()


if __name__ == '__main__':
    VideoRecorder.start_recording([0, 1])

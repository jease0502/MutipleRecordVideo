import os
import cv2
import gc
from multiprocessing import Process, Manager

def write(stack, cam, top: int) -> None:
    """
    :param cam: 攝影機編號
    :param stack: Manager.Queue()
    :param top: 緩衝
    :return: None
    """
    print('Process to write: %s' % os.getpid())
    cap = cv2.VideoCapture(cam,cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 15)

    while True:
        ret, img = cap.read()
        if not ret:
            continue
        stack.put(img)

def save(stack, cam_id) -> None:
    print('Process to save: %s' % os.getpid())
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    output_video = cv2.VideoWriter(
                f"{cam_id}" + '.avi', codec, 30, (640, 480))
    while True:
        frame = stack.get(True) # blocking operation
        output_video.write(frame)
        cv2.imshow(f"cam {cam_id} img", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            output_video.release()
            break

if __name__ == '__main__':

    q = Manager().Queue()
    q1 = Manager().Queue()
    pw = Process(target=write, args=(q, 1, 100))
    ps = Process(target=save, args=(q, 1))
    pw1 = Process(target=write, args=(q1, 0, 100))
    ps1 = Process(target=save, args=(q1, 0))
    
    pw.start()
    pw1.start()
    ps.start()
    ps1.start()
    ps.join()
    ps1.join()
    pw.terminate()
    pw1.terminate()

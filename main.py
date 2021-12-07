from threading import Thread
import cv2
import time


class VideoWriterWidget(object):
    def __init__(self, video_file_name, src=0):
        """
        Create a VideoCapture object
        if using webcams, else just use src as it is.
        """
        self.frame_name = str(src)
        self.video_file = video_file_name
        self.video_file_name = video_file_name + '.avi'
        self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.output_video = cv2.VideoWriter(
            self.video_file_name, self.codec, 30, (self.frame_width, self.frame_height))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        # Start another thread to show/save frames
        self.start_recording()
        print('initialized {}'.format(self.video_file))

    def update(self):
        """
        Read the next frame from the stream in a different thread
        """
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        """
        Display frames in main program
        """
        if self.status:
            cv2.imshow(self.frame_name, self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        """
        Save obtained frame into video output file
        """
        self.output_video.write(self.frame)

    def start_recording(self):
        """
        Create another thread to show/save frames
        """
        def start_recording_thread():
            while True:
                try:
                    self.show_frame()
                    self.save_frame()
                except AttributeError:
                    pass
        self.recording_thread = Thread(target=start_recording_thread, args=())
        self.recording_thread.daemon = True
        self.recording_thread.start()


if __name__ == '__main__':
    video_writer_widget = list()
    for i in range(int(input("pls input how many camera you are: "))):
        video_writer_widget.append(VideoWriterWidget('Camera' + str(i), i))

    while True:
        time.sleep(5)

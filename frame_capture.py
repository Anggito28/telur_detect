import time
import threading, queue
import numpy as np
import cv2

# camera Thread

class Camera_Thread:
    # camera setup
    camera_source = 0
    camera_width = 640
    camera_height = 480
    camera_frame_rate = 30
    camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # camera_fourcc = cv2.VidoeWriter_fourcc(*"YUYV")

    # buffer setup
    buffer_length = 5
    buffer_all = False

    # camera
    camera = None
    camera_init = 0.5

    # buffer
    buffer = None

    # control states
    frame_grab_run = False
    frame_grab_on = False

    # counts and amounts
    frame_count = 0
    frames_returned = 0
    current_frame_rate = 0
    loop_start_time = 0

    def start(self):

        # buffer
        if self.buffer_all:
            self.buffer = queue.Queue(self.buffer_length)
        else:
            self.buffer = queue.Queue(1)

        # camera setup
        self.camera = cv2.VideoCapture(self.camera_source)
        self.camera.set(3,self.camera_width)
        self.camera.set(4,self.camera_height)
        self.camera.set(5,self.camera_frame_rate)
        self.camera.set(6,self.camera_fourcc)
        time.sleep(self.camera_init)

        # camera image vars
        self.camera_width = int(self.camera.get(3))
        self.camera_height = int(self.camera.get(4))
        self.camera_frame_rate = int(self.camera.get(5))
        self.camera_mode = int(self.camera.get(6))
        self.camera_area = self.camera_width * self.camera_height

        # black frame (filler)
        self.black_frame = np.zeros((self.camera_height, self.camera_width,3),np.uint8)

        # set run state
        self.frame_grab_run = True

        # start
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        # set loop kill state
        self.frame_grab_run = False

        # loop stop
        while self.frame_grab_on:
            time.sleep(0.1)

        # stop camera
        if self.camera:
            try:
                self.camera.release()
            except:
                pass
        self.camera = None

        # drop bugger
        self.buffer = None

    def loop(self):
        # load start frame
        frame = self.black_frame
        if not self.buffer.full():
            self.buffer.put(frame,False)


        # status
        self.frame_grab_on = True
        self.loop_start_time = time.time()

        # frame rate
        fc = 0
        t1 = time.time()

        # looping
        while 1:
            if not self.frame_grab_run: #external shut down
                break

            if self.buffer_all: #buffered mode

                # buffer full
                if self.buffer.full():
                    time.sleep(1/self.camera_frame_rate)

                else:

                    grabbed,frame = self.camera.read()

                    if not grabbed:
                        break

                    self.buffer.put(frame,False)
                    self.frame_count += 1
                    fc += 1

            # false buffer mode
            else:

                grabbed,frame = self.camera.read()
                if not grabbed:
                    break

                if self.buffer.full():
                    self.buffer.get()


                self.buffer.put(frame, False)
                self.frame_count += 1
                fc += 1

            # update frame read rate
            if fc >= 10:
                self.current_frame_rate = round(fc/(time.time()-t1),2)
                fc = 0
                t1 = time.time()


        # shut down
        self.loop_start_time = 0
        self.frame_grab_on = False
        self.stop()

    def next(self,black=True,wait=0):

        # black frame default
        if black:
            frame = self.black_frame

        else:
            frame = None


        try:
            frame = self.buffer.get(timeout=wait)
            self.frames_returned += 1
        except queue.Empty:
            # print('Queue Empty')
            # print(tracback.format_exc())
            pass

        # done
        return frame
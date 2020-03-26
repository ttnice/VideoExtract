import cv2, pytesseract
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class Video:
    def __init__(self, path, breaker, error=.96):

        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.ret, self.frame = self.cap.read()

        # frame and second
        self.frame_found = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.sound_find = 0

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.second = 0

        self.total_time = self.frame_found*self.fps
        self.last_frame = np.empty((720, 1280, 3))

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Cutting image
        self.up = 0
        self.down = self.height
        self.left = 0
        self.right = self.width

        # Init
        self.last_text = ''
        self.current_frame = 0
        self.last_frame = None
        self.val_error = error
        self.breaker = breaker
        self.first_time = True

        self.current_chapter = 0

    def cutter(self, crop):
        time = int(self.fps*crop)
        for i in range(time):
            self.cap.read()
            self.current_frame += 1

    def cropper(self):
        ret, frame = self.cap.read()
        self.current_frame += 1
        while True:
            try:
                up, down, left, right = input('Enter "up, down, left, right" cropping : ').split(',')
                up, down, left, right = float(up), float(down), float(left), float(right)
                self.auto_crop(up, down, left, right)
                cut_frame = frame[self.up:self.down, self.left:self.right, :]
                plt.imshow(cut_frame)
                plt.show()
                if input('Enter "ok" if cropping ok : ') == 'ok':
                    break
            except:
                pass

    def auto_crop(self, up, down, left, right):
        self.up = int(self.height * up)
        self.down = int(-self.height * down) + self.height
        self.left = int(self.width * left)
        self.right = int(-self.width * right) + self.width



    def get(self):
        # reading from frame
        ret, frame = self.cap.read()
        if ret:
            cut_frame = frame[self.up:self.down, self.left:self.right, :]
            if self.first_time:
                self.last_frame = np.empty(cut_frame.shape)
                self.first_time = False
                for i in cut_frame.shape:
                    self.val_error *= i
            self.current_frame += 1

            # pass frame analyse, if frame is looking like last frame
            if np.sum(self.last_frame == cut_frame) <= self.val_error:
                # writing the extracted images
                image = Image.fromarray(cut_frame)
                text = pytesseract.image_to_string(image)
                # text = text.replace('\n', ' ')
                text = text.replace('|', 'I')

                # increasing counter so that it will
                # show how many frames are created
                self.last_frame = cut_frame
                self.frame_found += 1

                # pass text return, if last text is like last text
                if self.last_text != text:
                    print(text)
                    if self.breaker in text:
                        self.current_chapter += 1
                    self.last_text = text

                    return ret, True, self.current_chapter, text, self.current_frame/self.fps
            return ret, False, None, None, None
        else:
            return ret, False, None, None, None

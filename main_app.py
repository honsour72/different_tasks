from tkinter import *
import cv2
from PIL import ImageTk, Image


class MainApp:
    def __init__(self):
        self.root = Tk()
        self.left_camera = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.right_camera = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

        # 1
        self.root.title("Hello world")
        self.root.geometry("1400x700+100+100")

        # 2
        self.label_cameras_frame = LabelFrame(self.root, text="Cameras' eyes", height=550)
        self.label_cameras_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.label_buttons_frame = LabelFrame(self.root, text="Control buttons")
        self.label_buttons_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        # 3
        self.right_camera_label = Label(self.label_cameras_frame)
        self.right_camera_label.pack(side=RIGHT)

        self.left_camera_label = Label(self.label_cameras_frame)
        self.left_camera_label.pack(side=LEFT)

        # 4
        self.correct_button = Button(self.label_buttons_frame, text="Correct", command=self.take_photo_1)
        self.correct_button.pack(side=TOP, pady=10)

        self.orientation_button = Button(self.label_buttons_frame, text="Orientation", command=self.take_photo_2)
        self.orientation_button.pack(side=TOP, pady=10)

        # 5
        self.update_cameras()

    def update_cameras(self):
        self.left_camera_image = self.left_camera_movie()
        self.right_camera_image = self.right_camera_movie()

        self.left_camera_label.configure(image=self.left_camera_image)
        self.right_camera_label.configure(image=self.right_camera_image)

        self.left_camera_label.after(20, self.update_cameras)

    def left_camera_movie(self):
        ret, self.left_frame = self.left_camera.read()
        self.left_frame = cv2.flip(self.left_frame, 1)
        cv2image = cv2.cvtColor(self.left_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        return ImageTk.PhotoImage(img)

    def right_camera_movie(self):
        ret, self.right_frame = self.right_camera.read()
        self.right_frame = cv2.flip(self.right_frame, 1)
        cv2image = cv2.cvtColor(self.right_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        return ImageTk.PhotoImage(img)

    def take_photo_1(self, text_="correction"):
        left_file = "{} left.jpg".format(text_)
        right_file = "{} right.jpg".format(text_)
        cv2.imwrite(filename=left_file, img=self.left_frame)
        cv2.imwrite(filename=right_file, img=self.right_frame)

    def take_photo_2(self, text_="orientation"):
        left_file = "{} left.jpg".format(text_)
        right_file = "{} right.jpg".format(text_)
        cv2.imwrite(filename=left_file, img=self.left_frame)
        cv2.imwrite(filename=right_file, img=self.right_frame)

    def our_mainloop(self):
        self.root.mainloop()


def run():
    root = MainApp()
    root.our_mainloop()


if __name__== "__main__":
    run()



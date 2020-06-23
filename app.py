# The main purpose of the OS module is to interact with your operating system. The primary use I find for it is to
# create folders, remove folders, move folders, and sometimes change the working directory. You can also access the
# names of files within a file path by doing listdir()
import os
import random
import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound

WINDOW_TITLE = "My Wardrobe"
WINDOW_WIDTH = "500"
WINDOW_HEIGHT = "650"
IMG_WIDTH = 250
IMG_HEIGHT = 250
# store all tops into a file to access it and skip all hidden files
ALL_TOPS = [str('tops/') + image for image in os.listdir('tops/') if not image.startswith('.')]
ALL_BOTTOMS = [str('bottoms/') + image for image in os.listdir('bottoms/') if not image.startswith('.')]


class Wardrobe:

    def __init__(self, root):
        self.root = root

        # show tops in the top window
        self.top_images = ALL_TOPS
        self.bottom_images = ALL_BOTTOMS

        # save single top
        self.top_image_path = self.top_images[1]
        self.bottom_image_path = self.bottom_images[1]

        # create and add tops and bottoms into top frame
        self.top_frame = tk.Frame(self.root, background='wheat4')

        # stretch frame to the size of the window
        self.top_frame.grid(row=0, column=0, sticky="NESW")
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)
        # self.top_frame.grid_rowconfigure(3, weight=1)
        # self.top_frame.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.top_image_label = self.create_photo(self.top_image_path, self.top_frame)
        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.top_frame)
        self.top_title = tk.Message(self.top_frame, text="OUTFITS", width=100, foreground="White", background="wheat4")

        # add it to pack
        self.top_image_label.grid(row=1, column=1, pady=13)
        self.bottom_image_label.grid(row=3, column=1, pady=13)
        self.top_title.grid(row=0, column=1, pady=8)

        # create background
        self.create_background()

    def create_background(self):
        # add title and change window size
        self.root.title(WINDOW_TITLE)
        self.root.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # add all buttons
        self.create_buttons()

    def create_buttons(self):
        top_prev_button_top = tk.Button(self.top_frame, text="Prev", command=self.get_prev_top)
        top_prev_button_top.grid(row=2, column=0)

        top_next_button_top = tk.Button(self.top_frame, text="Next", command=self.get_next_top)
        top_next_button_top.grid(row=2, column=2)

        generate_outfit_button = tk.Button(self.top_frame, text="Generate outfit", command=self.get_next_outfit)
        generate_outfit_button.grid(row=2, column=1)

        top_prev_button_bottom = tk.Button(self.top_frame, text="Prev", command=self.get_prev_bottom)
        top_prev_button_bottom.grid(row=5, column=0, pady=10)

        top_next_button_bottom = tk.Button(self.top_frame, text="Next", command=self.get_next_bottom)
        top_next_button_bottom.grid(row=5, column=2, pady=10)

    def get_next_item(self, current_item, category, increment=True):
        item_index = category.index(current_item)
        final_index = len(category) - 1

        # consider edge cases
        if increment and item_index == final_index:
            next_index = 0
        elif not increment and item_index == 0:
            next_index = final_index
        else:
            if increment:
                increment = 1
            else:
                increment = -1
            next_index = item_index + increment

        next_image = category[next_index]

        # reset and update the image based on next_image path
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.top_image_path = next_image

        if current_item in self.bottom_images:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        # use update function to change the image
        self.update_image(next_image, image_label)

    def get_next_top(self):
        self.get_next_item(self.top_image_path, self.top_images)

    def get_prev_top(self):
        self.get_next_item(self.top_image_path, self.top_images, increment=False)

    def get_next_bottom(self):
        self.get_next_item(self.bottom_image_path, self.bottom_images)

    def get_prev_bottom(self):
        self.get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def update_image(self, new_image_path, image_label):
        # collect and change img into tk photo object
        image_file = Image.open(new_image_path)
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        tk_photo = ImageTk.PhotoImage(image_resized)

        # update based on provided image label
        image_label.configure(image=tk_photo)
        image_label.image = tk_photo

    def get_next_outfit(self):
        random_top = self.top_images[random.randrange(0, len(self.top_images))]
        random_bottom = self.bottom_images[random.randrange(0, len(self.bottom_images))]
        self.update_image(random_top, self.top_image_label)
        self.update_image(random_bottom, self.bottom_image_label)

    def create_photo(self, image_path, frame):
        # open the image
        image_file = Image.open(image_path)

        # resize it
        image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)

        # connect the photo to the label
        tk_photo = ImageTk.PhotoImage(image_resized)
        image_label = tk.Label(frame, image=tk_photo, relief='raised')
        image_label.image = tk_photo

        # so that we can add later
        return image_label


root = tk.Tk()
app = Wardrobe(root)
root.mainloop()

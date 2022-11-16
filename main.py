from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw
import cv2
import numpy as np

window = Tk()
window.title('Anh Minh')
window.geometry('800x400')

my_menu = Menu(window)
window.config(menu=my_menu)

# Click command


def new_file():
    global img, label, img_tk, root_img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    root_img = img
    img_resized = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img_resized)
    label = Label(window, image=img_tk)
    label.pack()


def save_file():
    global img
    rgb_img = img.convert('RGB')
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    rgb_img.save(filename)
# Create a menu item


def flipping_image():
    global img, label, img_flipped
    img_flipped = img.transpose(
        Image.Transpose.FLIP_LEFT_RIGHT).resize((400, 400))
    img_flipped_tk = ImageTk.PhotoImage(img_flipped)
    img = ImageTk.getimage(img_flipped_tk)
    label.configure(image=img_flipped_tk)
    label.image = img_flipped_tk


def rotateApplyButton():
    global txt, img, label, img_rotated_tk, window2
    img_rotated = img.rotate(float(txt.get()), expand=True).resize((400, 400))
    window2.destroy()
    img_rotated_tk = ImageTk.PhotoImage(img_rotated)
    img = ImageTk.getimage(img_rotated_tk)
    label.configure(image=img_rotated_tk)
    label.image = img_rotated_tk


def rotate():
    global txt, window2
    window2 = Tk()
    txt = Entry(window2, width=20)
    txt.grid(column=0, row=1)
    btn = Button(window2, text='Apply', command=rotateApplyButton)
    btn.grid(column=1, row=1)
    window2.mainloop()


cropping = False


x_start, y_start, x_end, y_end = 0, 0, 0, 0
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping, img, img_cv2
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2:  # when two points were found
            img_cv2 = img_cv2[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]


def crop():
    global img, label, img_cv2, i, x_start, x_end, y_start, y_end, cropping
    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    i = img_cv2.copy()
    cv2.namedWindow('crop')
    cv2.setMouseCallback('crop', mouse_crop)
    while (1):
        cv2.rectangle(i, (x_start, y_start),
                      (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow('crop', i)
        if cv2.getWindowProperty('crop', cv2.WND_PROP_VISIBLE) <1:
            break
        if cv2.waitKey(1) & 0xFF==27:
            x_start, y_start, x_end, y_end = 0, 0, 0, 0
            img = Image.fromarray(img_cv2).convert('RGB')
            data = np.array(img)
            red, green, blue = data.T
            data = np.array([blue, green, red])
            data = data.transpose()
            img = Image.fromarray(data)
            img_tk = ImageTk.PhotoImage(img.resize((400, 400)))
            label.configure(image=img_tk)
            label.image = img_tk
            break
    cv2.destroyAllWindows()


drawing = False  # true if mouse is pressed
pt1_x, pt1_y = None, None


def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y, drawing, a

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(a, (pt1_x, pt1_y), (x, y),
                     color=(255, 255, 255), thickness=3)
            pt1_x, pt1_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(a, (pt1_x, pt1_y), (x, y),
                 color=(255, 255, 255), thickness=3)


def draw():
    global img, a, label
    opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    a = np.asarray(opencvImage)
    cv2.namedWindow('draw')
    cv2.setMouseCallback('draw', line_drawing)
    while (1):
        cv2.imshow('draw', a)
        if cv2.getWindowProperty('draw', cv2.WND_PROP_VISIBLE) <1:
            break
        if cv2.waitKey(1) & 0xFF==27:
            img = Image.fromarray(a).convert('RGB')
            data = np.array(img)
            red, green, blue = data.T
            data = np.array([blue, green, red])
            data = data.transpose()
            img = Image.fromarray(data)
            img_tk = ImageTk.PhotoImage(img.resize((400, 400)))
            label.configure(image=img_tk)
            label.image = img_tk
            break
    cv2.destroyAllWindows()


def applyBlurFilter():
    global img, label
    img_blur = img.filter(ImageFilter.BLUR).resize((400, 400))
    img_blur_tk = ImageTk.PhotoImage(img_blur)
    img = ImageTk.getimage(img_blur_tk)
    label.configure(image=img_blur_tk)
    label.image = img_blur_tk


def applyContourFilter():
    global img, label
    img_contour = img.filter(ImageFilter.CONTOUR).resize((400, 400))
    img_contour_tk = ImageTk.PhotoImage(img_contour)
    img = ImageTk.getimage(img_contour_tk)
    label.configure(image=img_contour_tk)
    label.image = img_contour_tk


def applyDetailFilter():
    global img, label
    img_detail = img.filter(ImageFilter.DETAIL).resize((400, 400))
    img_detail_tk = ImageTk.PhotoImage(img_detail)
    img = ImageTk.getimage(img_detail_tk)
    label.configure(image=img_detail_tk)
    label.image = img_detail_tk


def applyEmbossFilter():
    global img, label
    img_emboss = img.filter(ImageFilter.EMBOSS).resize((400, 400))
    img_emboss_tk = ImageTk.PhotoImage(img_emboss)
    img = ImageTk.getimage(img_emboss_tk)
    label.configure(image=img_emboss_tk)
    label.image = img_emboss_tk


def applySharpenFilter():
    global img, label
    img_sharpen = img.filter(ImageFilter.SHARPEN).resize((400, 400))
    img_sharpen_tk = ImageTk.PhotoImage(img_sharpen)
    img = ImageTk.getimage(img_sharpen_tk)
    label.configure(image=img_sharpen_tk)
    label.image = img_sharpen_tk


def applySmoothFilter():
    global img, label
    img_smooth = img.filter(ImageFilter.SMOOTH).resize((400, 400))
    img_smooth_tk = ImageTk.PhotoImage(img_smooth)
    img = ImageTk.getimage(img_smooth_tk)
    label.configure(image=img_smooth_tk)
    label.image = img_smooth_tk


def applyBlackWhiteFilter():
    global img, label
    img_blackwhite = img.convert('L').resize((400, 400))
    img_blackwhite_tk = ImageTk.PhotoImage(img_blackwhite)
    img = ImageTk.getimage(img_blackwhite_tk)
    label.configure(image=img_blackwhite_tk)
    label.image = img_blackwhite_tk


def clear():
    global root_img, label, img
    img = root_img
    root_img_resized = root_img.resize((400, 400))
    root_img_tk = ImageTk.PhotoImage(root_img_resized)
    label.configure(image=root_img_tk)
    label.image = root_img_tk


def apply_adjust():
    global img, brightness_scale, r_scale, g_scale, b_scale
    r_value = r_scale.get()
    g_value = g_scale.get()
    b_value = b_scale.get()
    img_copy = img.copy()
    [xs, ys] = img_copy.size

    if not (r_value == 0 and g_value == 0 and b_value == 0):
        for x in range(0, xs):
            for y in range(0, ys):
                [r_, g_, b_] = img.getpixel((x, y))
                r_ = r_ + int(r_value)
                g_ = g_ + int(g_value)
                b_ = b_ + int(b_value)
                value = (r_, g_, b_)
                img_copy.putpixel((x, y), value)

    brightness_enhancer = ImageEnhance.Brightness(img_copy)
    img_copy = brightness_enhancer.enhance(brightness_scale.get())

    img_copy_tk = ImageTk.PhotoImage(img_copy.resize((400, 400)))
    label.configure(image=img_copy_tk)
    label.image = img_copy_tk
    img = ImageTk.getimage(img_copy_tk)
    window3.destroy()


def preview_adjust():
    global img, brightness_scale, r_scale, g_scale, b_scale
    r_value = r_scale.get()
    g_value = g_scale.get()
    b_value = b_scale.get()
    img_copy = img.copy()
    [xs, ys] = img_copy.size

    if not (r_value == 0 and g_value == 0 and b_value == 0):
        for x in range(0, xs):
            for y in range(0, ys):
                [r_, g_, b_] = img.getpixel((x, y))
                r_ = r_ + int(r_value)
                g_ = g_ + int(g_value)
                b_ = b_ + int(b_value)
                value = (r_, g_, b_)
                img_copy.putpixel((x, y), value)

    brightness_enhancer = ImageEnhance.Brightness(img_copy)
    img_copy = brightness_enhancer.enhance(brightness_scale.get())

    img_copy_tk = ImageTk.PhotoImage(img_copy.resize((400, 400)))
    label.configure(image=img_copy_tk)
    label.image = img_copy_tk


def cancel_adjust():
    global window3, img
    window3.destroy()
    img_tk = ImageTk.PhotoImage(img.resize((400, 400)))
    label.configure(image=img_tk)
    label.image = img_tk


def adjust():
    global window3, brightness_scale, r_scale, g_scale, b_scale
    window3 = Tk()
    brightness_label = Label(window3, text='Brightness')
    brightness_scale = Scale(window3, from_=0, to_=2, length=250,
                             resolution=0.1, orient=HORIZONTAL)
    r_label = Label(window3, text='R')
    r_scale = Scale(window3, from_=-100, to_=100, length=250,
                    resolution=1, orient=HORIZONTAL)
    g_label = Label(window3, text='G')
    g_scale = Scale(window3, from_=-100, to_=100, length=250,
                    resolution=1, orient=HORIZONTAL)
    b_label = Label(window3, text='B')
    b_scale = Scale(window3, from_=-100, to_=100, length=250,
                    resolution=1, orient=HORIZONTAL)
    apply_button = Button(window3, text='Apply', command=apply_adjust)
    preview_button = Button(window3, text='Preview', command=preview_adjust)
    cancel_button = Button(window3, text='Cancel', command=cancel_adjust)
    brightness_scale.set(1)
    brightness_label.pack()
    brightness_scale.pack()
    r_label.pack()
    r_scale.pack()
    g_label.pack()
    g_scale.pack()
    b_label.pack()
    b_scale.pack()
    cancel_button.pack(side=RIGHT)
    preview_button.pack(side=RIGHT)
    apply_button.pack()
    window3.mainloop()


file_menu = Menu(my_menu)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New...', command=new_file)
file_menu.add_separator()
file_menu.add_command(label='Save', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=window.quit)

edit_menu = Menu(my_menu)
my_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Flip', command=flipping_image)
edit_menu.add_separator()
edit_menu.add_command(label='Rotate', command=rotate)
edit_menu.add_separator()
edit_menu.add_command(label='Crop', command=crop)
edit_menu.add_separator()
edit_menu.add_command(label='Draw', command=draw)

filters_menu = Menu(my_menu)
my_menu.add_cascade(label='Filter', menu=filters_menu)
filters_menu.add_command(label='BLUR', command=applyBlurFilter)
filters_menu.add_separator()
filters_menu.add_command(label='CONTOUR', command=applyContourFilter)
filters_menu.add_separator()
filters_menu.add_command(label='Detail', command=applyDetailFilter)
filters_menu.add_separator()
filters_menu.add_command(label='Emboss', command=applyEmbossFilter)
filters_menu.add_separator()
filters_menu.add_command(label='Sharpen', command=applySharpenFilter)
filters_menu.add_separator()
filters_menu.add_command(label='Smooth', command=applySmoothFilter)
filters_menu.add_separator()
filters_menu.add_command(label='Black White', command=applyBlackWhiteFilter)

my_menu.add_cascade(label='Adjust', command=adjust)

my_menu.add_cascade(label='Clear', command=clear)
window.mainloop()

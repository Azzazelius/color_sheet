from PIL import Image, ImageStat
import numpy as np
import cv2

def calculate_average_color(im_piece):
    cv2_im = cv2.cvtColor(np.array(im_piece), cv2.COLOR_RGB2BGR)
    hsv_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_im)
    h_mean = cv2.mean(h)[0]
    s_mean = cv2.mean(s)[0]
    v_mean = cv2.mean(v)[0]
    return s_mean

im = Image.open("/home/alan/Pictures/colors_1.jpg")

piece_size = (192, 356)
max_width = 2560

# cut image to the pieces and organise them into a list
im_list = []
for x in range(0, im.width, piece_size[0]):
    for y in range(0, im.height, piece_size[1]):
        im_piece = im.crop((x, y, x + piece_size[0], y + piece_size[1]))
        im_list.append(im_piece)

im_list.sort(key=calculate_average_color, reverse=False)

result_width = min(len(im_list) * piece_size[0], max_width)
result_height = ((len(im_list) * piece_size[0]) + (max_width - 1)) // max_width * piece_size[1]

img_result = Image.new("RGB", (result_width, result_height), (255, 255, 255))

for i, im_piece in enumerate(im_list):
    x = (i % (result_width // piece_size[0])) * piece_size[0]
    y = (i // (result_width // piece_size[0])) * piece_size[1]
    img_result.paste(im_piece, (x, y))

# img_result.show()
img_result.save(f"/home/alan/Pictures/colors_S.jpg")

















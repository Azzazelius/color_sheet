from PIL import Image, ImageStat
import numpy as np
import cv2



# =================================== show image
# im = Image.open("/home/alan/Pictures/test2.jpg")
# print(im.format, im.size, im.mode)
# im.show()


# ================================= save renamed copy
# im_path = "/home/alan/Pictures/test2.jpg"
# im = Image.open(im_path)
#
# f, e = os.path.splitext(im_path)
# to_save = f + "upd" + ".jpg"
# im.save(to_save)

# ============================ combine to images to one
# im = Image.open("/home/alan/Pictures/test2.jpg")
# box = (160, 100, 380, 365) # 1, 2  - coordinates for upper left corner, 3,4 -  for lower right
# region = im.crop(box)
# # создаем новое изображение шириной, равной сумме ширин img1 и img2, и высотой img1
# new_img = Image.new('RGB', (region.width + region.width, region.height), (0, 0, 0))
# new_img.paste(region, (0, 0))
# new_img.paste(region, (region.width, 0))
# new_img.show()

# ==========================================================================================
# =================================== cut image to pieces and organize them into the line
# ==========================================================================================

# im = Image.open("/home/alan/Pictures/test2.jpg")
# piece_size = 20
# im_list = []
# for x in range(0, im.width, piece_size):
#     for y in range(0, im.height, piece_size):
#         im_piece = im.crop((x, y, x + piece_size, y + piece_size))
#         im_list.append(im_piece)
#
# result_width = len(im_list) * piece_size
# result_height = piece_size
# img_result = Image.new("RGB", (result_width, result_height))
#
# for index, im_piece in enumerate(im_list):
#     img_result.paste(im_piece, (index * piece_size, 0))
#
# img_result.show()
#
# ==========================================================================================
# =================================== organise into fixed lenght image
# ==========================================================================================
#
# im = Image.open("/home/alan/Pictures/test2.jpg")
# piece_size = 60
# max_width = 640
#
# #  cut image to the pieces and organise them into a list
# im_list = []
# for x in range(0, im.width, piece_size):
#     for y in range(0, im.height, piece_size):
#         im_piece = im.crop((x, y, x + piece_size, y + piece_size))
#         im_list.append(im_piece)
#
# result_width = min(len(im_list) * piece_size, max_width)  # final width is a min value between actual len and 640
# result_height = ((len(im_list) * piece_size) + (max_width-1)) // max_width * piece_size  # height = max len (all pieces in one line) + 639 // devision without reminder (it gives the number of lines)  * piece_size (gives the final height of all lines)
#
# img_result = Image.new("RGB", (result_width, result_height))
#
# for i, im_piece in enumerate(im_list):
#     # x = (i * piece_size) % result_width
#     # y = ((i * piece_size) // result_width) * piece_size
#     x = (i % (result_width // piece_size)) * piece_size
#     y = (i // (result_width // piece_size)) * piece_size
#     img_result.paste(im_piece, (x, y))
#
# img_result.show()


# ==========================================================================================
# =================================== ordered by color
# ==========================================================================================
#
#
# im = Image.open("/home/alan/Pictures/test2.jpg")
# piece_size = 100
# max_width = 640
#
# # cut image to the pieces and organize them into a list
# im_list = []
# for x in range(0, im.width, piece_size):
#     for y in range(0, im.height, piece_size):
#         im_piece = im.crop((x, y, x + piece_size, y + piece_size))
#         # compute average color for the piece
#         avg_color = ImageStat.Stat(im_piece).mean
#         im_list.append((im_piece, avg_color))
#
# # sort pieces by average color from red to violet
# im_list.sort(key=lambda x: (x[1][0], -x[1][1], -x[1][2]))
#
# # create a new image and paste the sorted pieces
# result_width = min(len(im_list) * piece_size, max_width)
# result_height = ((len(im_list) * piece_size) + (max_width - 1)) // max_width * piece_size
#
# img_result = Image.new("RGB", (result_width, result_height))
#
# for i, (im_piece, _) in enumerate(im_list):
#     x = (i % (result_width // piece_size)) * piece_size
#     y = (i // (result_width // piece_size)) * piece_size
#     img_result.paste(im_piece, (x, y))
#
# img_result.show()



def calculate_average_color(im_piece):
    stat = ImageStat.Stat(im_piece)
    r, g, b = stat.mean
    return r, g, b


def calculate_average_color_four(im_piece):
    r, g, b = 0, 0, 0
    count = 0
    for i in range(im_piece.width):
        for j in range(im_piece.height):
            pixel = im_piece.getpixel((i, j))
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
            count += 1
    return r / count, g / count, b / count


def calculate_average_color_numpy(im_piece):
    np_im = np.array(im_piece)
    r = np.mean(np_im[:,:,0])
    g = np.mean(np_im[:,:,1])
    b = np.mean(np_im[:,:,2])
    return r, g, b


def calculate_average_color_opencv(im_piece):
    cv2_im = cv2.cvtColor(np.array(im_piece), cv2.COLOR_RGB2BGR)
    avg_color = cv2.mean(cv2_im)
    r, g, b = avg_color[:3]
    return r, g, b


im = Image.open("/home/alan/PycharmProjects/Color_project/colors.jpg")

piece_size = (192, 356)
max_width = 2560

# cut image to the pieces and organise them into a list
im_list = []
for x in range(0, im.width, piece_size[0]):
    for y in range(0, im.height, piece_size[1]):
        im_piece = im.crop((x, y, x + piece_size[0], y + piece_size[1]))
        im_list.append(im_piece)


def sorting(sort_method, new):
    im_list.sort(key=sort_method, reverse=False)

    result_width = min(len(im_list) * piece_size[0], max_width)
    result_height = ((len(im_list) * piece_size[0]) + (max_width - 1)) // max_width * piece_size[1]

    img_result = Image.new("RGB", (result_width, result_height))

    for i, im_piece in enumerate(im_list):
        x = (i % (result_width // piece_size[0])) * piece_size[0]
        y = (i // (result_width // piece_size[0])) * piece_size[1]
        img_result.paste(im_piece, (x, y))

    # img_result.show()
    img_result.save(f"/home/alan/PycharmProjects/Color_project/colors_result_{new}.jpg")


sorting(calculate_average_color, "new")
sorting(calculate_average_color_four, "four")
sorting(calculate_average_color_numpy, "numpy")
sorting(calculate_average_color_opencv, "opencv")





import cv2
import numpy as np
import matplotlib.pyplot as plt

from canny_func import region_of_interest, make_points, average, display_lines


# def region(image):
#     height, width = image.shape
#     triangle = np.array([
#         [(100, height), (475, 325), (width, height)]
#     ])

#     mask = np.zeros_like(image)

#     mask = cv2.fillPoly(mask, triangle, 255)
#     mask = cv2.bitwise_and(image, mask)
#     return mask

# def roi_rec(img):
#     H, W = img.shape

#     # Generate mask for ROI (Region of Interest)
#     mask = np.zeros((H, W))
#     ii = int(H/2)
#     for i in range(H):
#         if i > ii:
#             for j in range(W):
#                 mask[i, j] = 1

#     # plt.imshow(mask, cmap='gray')
#     # plt.title('GaussianBlur'), plt.xticks([]), plt.yticks([])
#     # plt.show()
#     # Extract edges in ROI
#     roi = img * mask

#     return roi


# def roi_tri(img):
#     H, W = img.shape

#     # Generate mask for ROI (Region of Interest)
#     mask = np.zeros((H, W))
#     ii = int(H/2)
#     for i in range(H):
#         for j in range(W):
#             if i > (H / W) * j and i > -(H / W) * j + H:
#                 mask[i, j] = 1

#     # plt.imshow(mask, cmap='gray')
#     # plt.title('GaussianBlur'), plt.xticks([]), plt.yticks([])
#     # plt.show()
#     # Extract edges in ROI
#     roi = img * mask

#     return roi


# Loading image and convert it into gray scale
img = cv2.imread("lane detection test images/frame.jpg")
cv2.imshow('input img', img)
cv2.waitKey(3000)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray img', gray)
cv2.waitKey(3000)
# plt.imshow(gray)
# plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# Gaussian Blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('Gaussian Blue', blur)
cv2.waitKey(3000)
# plt.imshow(blur, cmap='gray')
# plt.title('GaussianBlur'), plt.xticks([]), plt.yticks([])
# plt.show()

# Canny edge detector
edges = cv2.Canny(blur, 100, 200)
cv2.imshow('Canny edge', edges)
cv2.waitKey(3000)
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edge'), plt.xticks([]), plt.yticks([])
# plt.show()


# def region_of_interest(image):
#     height = image.shape[0]
#     polygons = np.array([[(200, height), (1100, height), (550, 250)]])
#     mask = np.zeros_like(image)
#     cv2.fillPoly(mask, polygons, 255)
#     masked_image = cv2.bitwise_and(image, mask)
#     return masked_image


roi = region_of_interest(edges)
cv2.imshow('ROI', roi)
cv2.waitKey(3000)
# plt.imshow(roi, cmap='gray')
# plt.title('Region of interest'), plt.xticks([]), plt.yticks([])
# plt.show()


lines = cv2.HoughLinesP(roi, 2, np.pi/180, 100,
                        np.array([]), minLineLength=40, maxLineGap=5)


# def make_points(image, average):
#     slope, y_int = average
#     y1 = image.shape[0]
#     y2 = int(y1 * (3/5))
#     x1 = int((y1 - y_int) // slope)
#     x2 = int((y2 - y_int) // slope)
#     return np.array([x1, y1, x2, y2])


# def average(image, lines):
#     left = []
#     right = []
#     for line in lines:
#         print(line)
#         x1, y1, x2, y2 = line.reshape(4)
#         parameters = np.polyfit((x1, x2), (y1, y2), 1)
#         slope = parameters[0]
#         y_int = parameters[1]
#         if slope < 0:
#             left.append((slope, y_int))
#         else:
#             right.append((slope, y_int))
#     right_avg = np.average(right, axis=0)
#     left_avg = np.average(left, axis=0)
#     left_line = make_points(image, left_avg)
#     right_line = make_points(image, right_avg)
#     return np.array([left_line, right_line])


# def display_lines(image, lines):
#     lines_image = np.zeros_like(image)
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line
#             cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
#     return lines_image


copy = np.copy(img)
averaged_lines = average(copy, lines)
black_lines = display_lines(copy, averaged_lines)
# combine the line image and the color image (copy*0.8 + black_lines*1 + 1)
lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
cv2.imshow('Result', lanes)
cv2.waitKey(3000)

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread("lane detection test images/frame.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('red', gray)
cv2.waitKey(3000)
cv2.imwrite('a/gray.jpg',gray)

# lower_red_hue_range = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
# plt.imshow(lower_red_hue_range)
# # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# upper_red_hue_range = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
# plt.imshow(upper_red_hue_range)
# # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# plt.show()


# red_hue_img = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
# plt.imshow(red_hue_img)
# # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# plt.show()

# blur = cv2.GaussianBlur(red_hue_img, (9, 9), 2, 2)
# plt.imshow(blur)
# # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# plt.show()




# canvas = np.zeros(shape=img.shape, dtype=np.uint8)
# canvas.fill(255)
# canvas[np.where((img == [161,77,80]).all(axis = 2))] = [255,0,0]
# # plt.imshow(canvas)
# # # # plt.title('Gray Image'), plt.xticks([]), plt.yticks([])
# # plt.show()
# cv2.imshow('red', canvas)
# cv2.waitKey(3000)


border, binary = cv2.threshold(gray, 30,110,cv2.THRESH_BINARY)
cv2.imshow('red', binary)
cv2.waitKey(3000)
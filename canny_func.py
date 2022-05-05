import cv2
import numpy as np
import matplotlib.pyplot as plt


def region_of_interest(image):
    height, width = image.shape
    print(height, width)
    # polygons = np.array([
    #     [(0, height), (int(width/2), int(height/6)), (width, height)]
    # ])
    polygons = np.array([
        [(0, height), (0, int(height/2)),
         (width, int(height/2)), (width, height)]
    ])
    mask = np.zeros_like(image)

    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def make_points(image, average):
    # try:
    #     slope, intercept = line_parameters
    # except TypeError:
    #     slope, intercept = 0,0
    slope, y_int = average
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)
    return np.array([x1, y1, x2, y2])


def average(image, lines):
    left = []
    right = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            # print(x1, y1, x2, y22
            # Finding parameters of a line
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            # print(parameters)
            slope = parameters[0]
            y_int = parameters[1]
            # Classify negative slope and positive slope
            if slope < 0:
                left.append((slope, y_int))
            else:
                right.append((slope, y_int))
        # Compute average of positive slope line and negative slope line
    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    # if left_avg:
    # put points in the image
    left_line = make_points(image, left_avg)
    # print(left_line)
    # if right_avg:
    right_line = make_points(image, right_avg)

    return np.array([left_line, right_line])


def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            print(line)
            x1, y1, x2, y2 = line
            cv2.line(lines_image, (x1, y1), (x2, y2), (0, 255, 0), 20)
    return lines_image

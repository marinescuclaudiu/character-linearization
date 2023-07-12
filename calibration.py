from box import Box
import numpy as np
import cv2
import skimage as ski
from scipy.signal import find_peaks
from decimal import Decimal

boxes = []

def read_boxes(input_path):
    with open(input_path, encoding='utf8') as file:
        for i, line in enumerate(file):
            values = line.strip().split()

            top_left_x = float(values[0])
            top_left_y = float(values[1])
            bot_right_x = float(values[2])
            bot_right_y = float(values[3])
            label = values[4]
            line_above = values[5]

            box = Box(i, top_left_x, top_left_y, bot_right_x, bot_right_y, label, line_above)
            boxes.append(box)


def find_rows(image_path, block_size=11, constant=10, sigma=None, height=300, distance=50):
    if sigma is None:
        sigma = [5, 50]

    grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    threshold_image = cv2.adaptiveThreshold(grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                            block_size, constant)

    max_value = np.max(threshold_image)
    inverted_image = max_value - threshold_image

    filtered_image = ski.filters.gaussian(inverted_image, sigma)

    histogram = np.sum(filtered_image[:, :], axis=1)
    peaks, _ = find_peaks(histogram, height=height, distance=distance)

    return peaks


def calibrate(rows_position, boxes):
    correct_boxes = 0
    remaining_boxes = []

    for box in boxes:
        y_center = Decimal(box.y_center)

        if y_center < Decimal(int(rows_position[0])):
            correct_boxes += 1
            continue

        elif y_center > Decimal(int(rows_position[len(rows_position) - 1])):
            correct_boxes += 1
            continue

        go_further = True
        for i in range(len(rows_position)):
            row = Decimal(int(rows_position[i]))
            if y_center == row:
                correct_boxes += 1
                go_further = False
                break

        if go_further is True:
            remaining_boxes.append(box)

    print(f"Total boxes {len(boxes)}")
    print(f"Correct boxes {correct_boxes}")
    print(f"Total boxes remained {len(remaining_boxes)}")

    w1 = Decimal('0')
    min_threshold = None
    max_threshold = None

    while w1 <= Decimal('0.99'):
        w2 = Decimal(1 - w1)

        for i, box in enumerate(remaining_boxes):
            y_center = Decimal(box.y_center)

            for j in range(len(rows_position) - 1):
                row_above = Decimal(int(rows_position[j]))
                row_below = Decimal(int(rows_position[j + 1]))

                if row_above < y_center < row_below:

                    f_above = Decimal((w1 * w2) / ((y_center - row_above) ** 2))

                    f_below = Decimal(w1 / (w2 * ((y_center - row_below) ** 2)))

                    if min_threshold is None or min_threshold > f_above:
                        min_threshold = Decimal(f_above)

                    if min_threshold is None or min_threshold > f_below:
                        min_threshold = Decimal(f_below)

                    if max_threshold is None or max_threshold < f_above:
                        max_threshold = Decimal(f_above)

                    if max_threshold is None or max_threshold < f_below:
                        max_threshold = Decimal(f_below)

                    break

        w1 += Decimal('0.01')

    result = []

    unit = Decimal((max_threshold - min_threshold) / 100)

    w1 = Decimal('0')
    while w1 <= Decimal('0.99'):
        w2 = Decimal(1 - w1)
        threshold = Decimal(min_threshold)

        while threshold <= max_threshold:
            boxes_found = 0
            for i, box in enumerate(remaining_boxes):
                y_center = Decimal(box.y_center)

                for j in range(len(rows_position) - 1):
                    row_above = Decimal(int(rows_position[j]))
                    row_below = Decimal(int(rows_position[j + 1]))

                    if row_above < y_center < row_below:

                        f_above = Decimal((w1 * w2) / ((y_center - row_above) ** 2))

                        f_below = Decimal(w1 / (w2 * ((y_center - row_below) ** 2)))

                        if f_above >= threshold > f_below and box.line_above == '1':
                            boxes_found += 1

                        if f_below >= threshold > f_above and box.line_above == '0':
                            boxes_found += 1

                        break

            result.append([w1, threshold, boxes_found])

            threshold += unit

        w1 += Decimal('0.01')

    best_values = max(result, key=lambda x: x[2])

    return best_values


read_boxes(r'C:\Users\claud\OneDrive\Desktop\CalibrationModel\fragment-hronograf.txt')

rows_position = find_rows(r'C:\Users\claud\OneDrive\Desktop\CalibrationModel\fragment-hronograf.jpg')

print(f'Rows positions at: {rows_position}')

best = calibrate(rows_position, boxes)

print(f'w1 {best[0]}, Threshold {best[1]}, Boxes found {best[2]}')

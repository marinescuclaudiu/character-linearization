import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage as ski
from scipy.signal import find_peaks


class RowFinder:
    def __init__(self):
        self.original_image = None
        self.grayscale_image = None
        self.output_path = None

    def set_output_path(self, output_path):

        self.output_path = output_path

    def save_image(self, image, image_name, is_gray=True):

        if is_gray:
            plt.imsave(os.path.join(self.output_path, image_name), image, cmap='gray')
        else:
            plt.imsave(os.path.join(self.output_path, image_name), image)

        plt.close()

    def read_image(self, image_path):

        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.save_image(self.original_image, 'original-image.jpg', False)

        self.grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.save_image(self.grayscale_image, 'grayscale-image.jpg')

    def adaptive_threshold(self, image, block_size=11, constant=10):

        threshold_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size,
                                                constant)

        self.save_image(threshold_image, 'adaptive-threshold-image.jpg')

        return threshold_image

    def invert_image(self, image):

        max_value = np.max(image)
        inverted_image = max_value - image

        self.save_image(inverted_image, 'inverted-image.jpg')

        return inverted_image

    def gaussian_filter(self, image, sigma=None):

        if sigma is None:
            sigma = [5, 50]

        filtered_image = ski.filters.gaussian(image, sigma)

        self.save_image(filtered_image, 'filtered-image.jpg')

        return filtered_image

    def find_peaks(self, image, height=300, distance=50):

        histogram = np.sum(image[:, :], axis=1)
        peaks, _ = find_peaks(histogram, height=height, distance=distance)

        return peaks

    def draw_lines(self, image, peaks):

        image_copy = np.copy(image)

        for peak in peaks:
            image_copy[peak, :] = (255, 0, 0)

        self.save_image(image_copy, 'row-lines-image.jpg', False)

    def find_rows(self):

        adaptive_threshold_image = self.adaptive_threshold(self.grayscale_image)

        inverted_image = self.invert_image(adaptive_threshold_image)

        filtered_image = self.gaussian_filter(inverted_image)

        peaks = self.find_peaks(filtered_image)

        self.draw_lines(self.original_image, peaks)

        return peaks

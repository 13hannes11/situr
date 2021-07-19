import abc
from PIL import Image, ImageDraw
from skimage import img_as_float
from skimage.feature import blob_dog
import numpy as np

from situr.image.situ_image import SituImage


class PeakFinder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        """Finds the peaks in the input image"""
        raise NotImplementedError(
            self.__class__.__name__ + '.find_peaks')

    def get_channel_peaks(self, img: SituImage, channel: int, focus_level: int = 0) -> np.ndarray:
        """Returns the coordinates of peaks (local maxima) in the specified channel and focus_level. It uses the self.

        Args:
            img (SituImage): The image to find the peaks on.
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.

        Returns:
            np.ndarray: np.ndarray: The peaks found by this method as np.array of shape (n, 2)
        """
        return self.find_peaks(img.get_data()[channel, focus_level, :, :])

    def show_channel_peaks(self, img: SituImage, channel: int, focus_level: int = 0, img_show=True) -> Image:
        """Returns and shows the found peaks drawn onto the image. Uses get_channel_peaks internally.

        Args:
            img (SituImage): The image to find the peaks on.
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.
            img_show (bool, optional): Specifies if img.show is to be called or if just the image should be returned. Defaults to True.

        Returns:
            Image: The image of the specified focus level and channel with encircled peaks.
        """
        peaks = self.get_channel_peaks(img, channel, focus_level)

        img = img.show_channel(
            channel, focus_level=focus_level, img_show=False).convert('RGB')
        draw = ImageDraw.Draw(img)

        width = 3
        inner_radius = 5
        outer_radius = inner_radius + width

        for x, y in zip(peaks[:, 0], peaks[:, 1]):
            draw.ellipse((x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius),
                         outline='navy', width=width)
            draw.ellipse((x - outer_radius, y - outer_radius, x + outer_radius, y + outer_radius),
                         outline='yellow', width=width)
        if img_show:
            img.show()
        return img


class PeakFinderDifferenceOfGaussian(PeakFinder):
    def __init__(self, min_sigma=0.75, max_sigma=3, threshold=0.1):
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.threshold = threshold

    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        img = img_as_float(img_array)
        peaks = blob_dog(img, min_sigma=self.min_sigma,
                         max_sigma=self.max_sigma, threshold=self.threshold)

        # Swap x and y
        peaks = peaks[:, [0, 1]] = peaks[:, [1, 0]]
        return peaks
import abc
from PIL import Image, ImageDraw
from skimage import img_as_float
from skimage.feature import blob_dog
import numpy as np
from matplotlib import pyplot as plt

from situr.image.situ_image import SituImage


class PeakFinder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        """Finds the peaks in the input image"""
        raise NotImplementedError(
            self.__class__.__name__ + '.find_peaks')

    def get_channel_peaks(self, img: SituImage, channel: int, focus_level: int = 0) -> np.ndarray:
        """Returns the coordinates of peaks (local maxima) in the specified channel and focus_level.
            It uses the method find_peaks.

        Args:
            img (SituImage): The image to find the peaks on.
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.

        Returns:
            np.ndarray: np.ndarray: The peaks found by this method as np.array of shape (n, 2)
        """
        return self.find_peaks(img.get_data()[channel, focus_level, :, :])

    def scatterplot_channel_peaks(self,
                                  img: SituImage,
                                  channel: int,
                                  focus_level: int = 0,
                                  color='b'):
        peaks = self.get_channel_peaks(img, channel, focus_level)

        # TODO: test with non square image if right coordinates
        plt.xlim(0, img.get_focus_level(0, 0).shape[1])
        plt.ylim(0, img.get_focus_level(0, 0).shape[0])
        plt.scatter(peaks[:, 0], peaks[:, 1], color=color)

    def show_channel_peaks(self,
                           img: SituImage,
                           channel: int,
                           focus_level: int = 0,
                           img_show=True) -> Image:
        """Returns and shows the found peaks drawn onto the image.
            Uses get_channel_peaks internally.

        Args:
            img (SituImage): The image to find the peaks on.
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.
            img_show (bool, optional): Specifies if img.show is to be called or if just the image
                should be returned. Defaults to True.

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
    """A class using difference of gaussian to find peaks. It uses skimage blob_dog internally.

    ...

    Attributes
    ----------
    min_sigma (float)
    max_sigma (int)
    threshold (float)
    """
    def __init__(self, min_sigma=0.75, max_sigma=3, threshold=0.1):
        """ For more detailed information about the parameters in the constructor
            refer to blob_dog from skimage.feature.

        Args:
            min_sigma (float, optional): Defaults to 0.75.
            max_sigma (int, optional): Defaults to 3.
            threshold (float, optional): Defaults to 0.1.
        """
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.threshold = threshold

    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        """Finds the peaks in the input image"""

        img = img_as_float(img_array)
        peaks = blob_dog(img, min_sigma=self.min_sigma,
                         max_sigma=self.max_sigma, threshold=self.threshold)

        # Swap x and y
        peaks = peaks[:, [0, 1]] = peaks[:, [1, 0]]
        return peaks

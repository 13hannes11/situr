import abc
from situr.transformation.transformation import Transform
import numpy as np
from PIL import Image, ImageDraw
from skimage import img_as_float
from skimage.feature import blob_dog

from typing import List

from situr.transformation import Transform, IdentityTransform


def extend_dim(array: np.ndarray):
    ones = np.ones((array.shape[0], 1))
    return np.append(array, ones, axis=1)


def remove_dim(array: np.ndarray):
    return array[:, :-1]


class PeakFinder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        """Finds the peaks in the input image"""
        raise NotImplementedError(
            self.__class__.__name__ + '.find_peaks')


class PeakFinderDifferenceOfGaussian(PeakFinder):
    def __init__(self, min_sigma=0.75, max_sigma=3, threshold=0.1):
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.threshold = threshold

    def find_peaks(self, img_array: np.ndarray) -> np.ndarray:
        img = img_as_float(img_array)
        peaks = blob_dog(img, min_sigma=self.min_sigma,
                         max_sigma=self.max_sigma, threshold=self.threshold)
        return peaks[:, 0:2]


class SituImage:
    """
    A class to representing one situ image with different focus levels.

    ...

    Attributes
    ----------
    data : numpy.array
        the image data containing all the channels of shape (channels, focus_levels, image_size_y, image_size_x)
    files :  List[List[str]] 
        A list of lists. Each inner list corresponds to one focus level. Its contents correspons to a file for each channel.
    nucleaus_channel : int
        tells which channel is used for showing where the cell nucleuses are.
    peak_finder : 
    """

    def __init__(self, file_list: List[List[str]], nucleaus_channel: int = 4, peak_finder: PeakFinder = PeakFinderDifferenceOfGaussian()):
        self.files = file_list
        self.data = None
        self.nucleaus_channel = nucleaus_channel
        self.channel_transformations = [
            IdentityTransform() for file in file_list
        ]
        self.peak_finder = peak_finder

    def get_data(self) -> np.ndarray:
        if self.data is None:
            self._load_image()
        return self.data

    def apply_transformations(self):
        for i, transformation in enumerate(self.channel_transformations):
            for focus_level in range(self.get_focus_level_count()):
                img = self.get_focus_level(i, focus_level)
                transformation.apply_tranformation(img)

    def apply_transform_to_whole_image(self, transform: Transform):
        for channel in range(self.get_channel_count()):
            for focus_level in range(self.get_focus_level_count()):
                img = self.get_focus_level(channel, focus_level)
                transform.apply_tranformation(img)

    def set_channel_transformation(self, channel: int, transformation: Transform):
        self.channel_transformations[channel] = transformation

    def get_channel_count(self) -> int:
        return self.get_data().shape[0]

    def get_focus_level_count(self) -> int:
        return self.get_data().shape[1]

    def get_focus_level(self, channel: int, focus_level: int) -> np.ndarray:
        """Loads channel and focus level of an image.

        Args:
            channel (int): The channel to be used
            focus_level (int): The focus level to be used

        Returns:
            np.ndarray: The loaded image of shape (width, height)
        """
        return self.get_data()[channel, focus_level, :, :]

    def get_channel(self, channel: int) -> np.ndarray:
        """Loads and returns the specified channel for all focus_levels.

        Args:
            channel (int): The channel to be returned

        Returns:
            np.ndarray: The loaded image of shape (focus_level, width, height)
        """
        return self.get_data()[channel, :, :, :]

    def _load_image(self):
        """Loads the whole image from files
        """
        image_list = []
        for focus_level_list in self.files:
            channels = []
            for file in focus_level_list:
                channels.append(np.array(Image.open(file)))
            image_list.append(channels)
        self.data = np.array(image_list)

    def unload_image(self):
        """Unloads the image data to free up memory
        """
        self.data = None

    def show_channel(self, channel: int, focus_level: int = 0) -> Image:
        """Prints and returns the specified channel and focus_level of the image.

        Args:
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.

        Returns:
            Image: The image of the specified focus level and channel
        """
        img = Image.fromarray(
            self.get_data()[channel, focus_level, :, :].astype(np.uint8))
        img.show()
        return img

    def get_channel_peaks(self, channel: int, focus_level: int = 0) -> np.ndarray:
        """Returns the coordinates of peaks (local maxima) in the specified channel and focus_level. It uses the self.

        Args:
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.

        Returns:
            np.ndarray: The peaks found by this method as np.array of shape (n, 2)
        """
        return self.peak_finder.find_peaks(self.get_data()[channel, focus_level, :, :])

    def show_channel_peaks(self, channel: int, focus_level: int = 0) -> Image:
        """Returns and shows the found peaks drawn onto the image. Uses get_channel_peaks internally.

        Args:
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.

        Returns:
            Image: The image of the specified focus level and channel with encircled peaks.
        """
        peaks = self.get_channel_peaks(
            channel, focus_level)

        img = Image.fromarray(
            self.get_data()[channel, focus_level, :, :].astype(np.uint8))
        draw = ImageDraw.Draw(img)
        for x, y in zip(peaks[:, 0], peaks[:, 1]):
            draw.ellipse((x - 5, y - 5, x + 5, y + 5),
                         outline='white', width=3)
        img.show()
        return img

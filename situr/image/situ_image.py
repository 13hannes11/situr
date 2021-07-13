import numpy as np
from PIL import Image, ImageDraw
from skimage import img_as_float
from skimage.feature import blob_dog

from situr.transformation.channel_transformation import IdentityChannelTransform


def extend_dim(array):
    ones = np.ones((array.shape[0], 1))
    return np.append(array, ones, axis=1)


def remove_dim(array):
    return array[:, :-1]


class PeakFinderDifferenceOfGaussian:
    def __init__(self, min_sigma=0.75, max_sigma=3, threshold=0.1):
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.threshold = threshold

    def find_peaks(self, img_array):
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
    files: (list(list(str))) 
        A list of lists. Each inner list corresponds to one focus level. Its contents correspons to a file for each channel.
    nucleaus_channel : int
        tells which channel is used for showing where the cell nucleuses are.
    """

    def __init__(self, file_list, nucleaus_channel=4):
        self.files = file_list
        self.data = None
        self.nucleaus_channel = nucleaus_channel
        self.channel_transformations = [
            IdentityChannelTransform() for file in file_list
        ]
        self.peak_finder = PeakFinderDifferenceOfGaussian()

    def get_data(self):
        if self.data is None:
            self._load_image()
            # TODO: apply transformations
        return self.data

    def apply_transformations():
        # TODO: implement
        pass

    def set_channel_transformation(self, channel, transformation):
        self.channel_transformations[channel] = transformation

    def get_channel_count(self):
        return self.get_data().shape[0]

    def get_focus_level_count(self):
        return self.get_data().shape[1]

    def get_focus_level(self, channel, focus_level):
        """Loads channel and focus level of an image.

        Args:
            channel (int): The channel to be used
            focus_level (int): The focus level to be used
        Returns: 
            numpy.array: The loaded image of shape (width, height)
        """
        return self.get_data()[channel, focus_level, :, :]

    def get_channel(self, channel):
        '''
        Loads and returns the specified channel for all focus_levels.

        Returns: 
            numpy.array: The loaded image of shape (focus_level, width, height)
        '''
        return self.get_data()[channel, :, :, :]

    def _load_image(self):
        '''
        Loads the channels of an image from seperate files and returns them as numpy array.

        Parameters:
            channel (int): 
                The channel that should be used
        Returns: 
            numpy.array: The loaded image of shape (channels, focus_level, width, height)
        '''
        image_list = []
        for focus_level_list in self.files:
            channels = []
            for file in focus_level_list:
                channels.append(np.array(Image.open(file)))
            image_list.append(channels)
        self.data = np.array(image_list)

    def unload_image(self):
        '''
        Unloads the image data to free up memory
        '''
        self.data = None

    def show_channel(self, channel, focus_level=0):
        '''
        Prints and returns the specified channel and focus_level of the image.

        Parameters:
            channel (int): 
                The channel that should be used when printing
            focus_level (int) default: 0:
                The focus level that should be used
        Returns:
            image: The image of the specified focus level and channel
        '''
        img = Image.fromarray(self.get_data()[0, 0, :, :])
        img.show()
        return img

    def get_channel_peaks(self, channel, focus_level=0, min_sigma=0.75, max_sigma=3, threshold=0.1):
        '''
        Returns the coordinates of peaks (local maxima) in the specified channel and focus_level. 
        This method uses skimage blob_dog, therefore using difference of gaussian.

        Parameters:
            channel (int): 
                The channel that should be used when printing
            focus_level (int) default: 0:
                The focus level that should be used
        Returns:
            np.array: The peaks found by this method as np.array of shape (n, 2)
        '''
        return self.peak_finder.find_peaks(self.get_data()[channel, focus_level, :, :])

    def show_channel_peaks(self, channel, focus_level=0):
        '''
        Returns and shows the found. Uses get_channel_peaks internally.

        Parameters:
            channel (int): 
                The channel that should be used when printing
            focus_level (int) default: 0:
                The focus level that should be used
        Returns:
            image: The image of the specified focus level and channel with encircled peaks.
        '''
        peaks = self.get_channel_peaks(
            channel, focus_level)

        img = Image.fromarray(self.get_data()[channel, focus_level, :, :])
        draw = ImageDraw.Draw(img)
        for x, y in zip(peaks[:, 0], peaks[:, 1]):
            draw.ellipse((x - 5, y - 5, x + 5, y + 5),
                         outline='white', width=3)
        img.show()
        return img

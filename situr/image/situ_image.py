import numpy as np
from PIL import Image
from typing import List

from situr.transformation import Transform, IdentityTransform


def extend_dim(array: np.ndarray) -> np.ndarray:
    """Extends the dimensions of a numpy array where ever value is 1.

    Args:
        array (np.ndarray): The array to extend the dimension from

    Returns:
        (np.ndarray): Slice of the modified array
    """
    ones = np.ones((array.shape[0], 1))
    return np.append(array, ones, axis=1)


def remove_dim(array: np.ndarray) -> np.ndarray:
    """Removes the last dimension of the numpy array

    Args:
        array (np.ndarray): The array to remove the last dimension from.

    Returns:
        (np.ndarray): Slice of the modified array
    """
    return array[:, :-1]


class SituImage:
    """
    A class to representing one situ image with different
    channels and focus levels. Another term for this is round.

    ...

    Attributes
    ----------
    data : numpy.array
        the image data containing all the channels of
        shape (channels, focus_levels, image_size_y, image_size_x)
    files :  List[List[str]]
        A list of lists. Each inner list corresponds to one focus level.
        Its contents correspons to a file for each channel.
    nucleaus_channel : int
        tells which channel is used for showing where the cell nucleuses are.
    channel_transformations : List[Transform]
        A list of transformations for each channel,
        wherby the index corresponds to the channel
    """

    def __init__(self, file_list: List[List[str]], nucleaus_channel: int = 4):
        """Initializes a situ image.

        Args:
            file_list (List[List[str]]): A list of Lists that specifies
                channels and focus levels. The inner list is for focus levels
                and each outer list is for the rounds. So if we have an image
                with two focus levels and 3 channels it would look like this:
                    [
                        ['ch0_f0.tif', 'ch0_f1.tif'],
                        [ch1_f0.tif', 'ch1_f1.tif'],
                        [ch2_f0.tif', 'ch2_f1.tif']
                    ]
            nucleaus_channel (int, optional): The channel that is showing the nucleai
                and not other data. Defaults to 4.
        """
        self.files = file_list
        self.data = None
        self.nucleaus_channel = nucleaus_channel
        self.channel_transformations = [
            IdentityTransform() for file in file_list
        ]

    def get_data(self) -> np.ndarray:
        """Returns the image data (also loads it if not yet in memory).

        Returns:
            np.ndarray: the image data in the shape (channel, focus_level, image_dim, image_dim)
        """
        if self.data is None:
            self._load_image()
        return self.data

    def apply_transformations(self):
        """Applies the stored transformations to the image.
        """
        for i, transformation in enumerate(self.channel_transformations):
            for focus_level in range(self.get_focus_level_count()):
                img = self.get_focus_level(i, focus_level)
                transformation.apply_tranformation(img)

    def apply_transform_to_whole_image(self, transform: Transform):
        """Applies an external transformation to every channel and focus level of an image.

        Args:
            transform (Transform): the transformation that will be applied
        """
        for channel in range(self.get_channel_count()):
            for focus_level in range(self.get_focus_level_count()):
                img = self.get_focus_level(channel, focus_level)
                transform.apply_tranformation(img)

    def set_channel_transformation(self, channel: int, transformation: Transform):
        """Sets a transformation for a channel, however does not apply it.

        Args:
            channel (int): The channel that the transformation should be applied to
            transformation (Transform): The transformation that will be applied to
                the specified channel
        """
        self.channel_transformations[channel] = transformation

    def get_channel_count(self) -> int:
        """Method to get the number of channels an image has.

        Returns:
            int: the number of channels
        """
        return self.get_data().shape[0]

    def get_focus_level_count(self) -> int:
        """Method to get the number of focus levels an image has.

        Returns:
            int: the number of focus levels
        """
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

    def show_channel(self, channel: int, focus_level: int = 0, img_show=True) -> Image:
        """Prints and returns the specified channel and focus_level of the image.

        Args:
            channel (int): The channel that should be used when printing
            focus_level (int, optional): The focus level that should be used. Defaults to 0.
            img_show (bool, optional): Specifies if img.show is to be called or if just the image
                should be returned. Defaults to True.

        Returns:
            Image: The image of the specified focus level and channel
        """
        img = Image.fromarray(
            self.get_data()[channel, focus_level, :, :].astype(np.uint8))
        if img_show:
            img.show()
        return img

from situr.transformation import Transform, IdentityTransform
import numpy as np

from situr.image.situ_image import SituImage

from typing import List


class Tile:
    """This class represents one tile. A tile consists of multiple rounds which each are
        represented by one SituImage.

    ...

    Attributes
    ----------
    images : SituImage
        the images representing the individual rounds.
    round_transformations :  List[Transform]
        A list containing transformations for each round (e.g. for registration).
    """

    def __init__(self, file_list: List[List[List[str]]], nucleaus_channel: int = 4):
        """The constructor for a tile.

        Args:
            file_list (List[List[List[str]]]): A list of lists  of list. Each list in the outer
                most list represents one round (SituImage). The following list represents on
                channel and the final list represents the focus levels (for more go to SituImage).
            nucleaus_channel (int, optional): The channel that contains information about nucleai.
                Defaults to 4.
        """
        self.images = []
        self.round_transformations = []
        for situ_image_list in file_list:
            self.images.append(
                SituImage(situ_image_list, nucleaus_channel=nucleaus_channel))
            self.round_transformations.append(IdentityTransform())

    def apply_transformations(self):
        """Method that first applies all round transformations
            and then all channel transformations.
        """
        self.apply_channel_transformations()
        self.apply_round_transformations()

    def apply_channel_transformations(self):
        """Method that apllies all stored channel transformations.
            It does not apply any round transformations.
        """
        for i in range(self.get_round_count()):
            self.images[i].apply_transformations()

    def apply_round_transformations(self):
        """Method that applies all stored transformations for each round.
            It doesn't apply channel transformations.
        """
        for round, transformation in enumerate(self.round_transformations):
            self.images[round].apply_transform_to_whole_image(transformation)

    def set_round_transformation(self, round: int, transformation: Transform):
        """Set the transformation for one round, however, does not apply it.

        Args:
            round (int): the round the transformation should be applied to
            transformation (Transform): the transformation for the round
        """
        self.round_transformations[round] = transformation

    def get_round_count(self) -> int:
        """Returns the number of rounds this tile has.

        Returns:
            int: the number of rounds
        """
        return len(self.images)

    def get_channel_count(self) -> int:
        """Returns the number of channels the tile has.

        Returns:
            int: the number of channels
        """
        return self.images[0].get_channel_count()

    def get_round(self, round_number: int) -> SituImage:
        """This methods returns the round based on round number

        Args:
            round_number (int): The round number (starting with index 0)

        Returns:
            SituImage: The image corresponding to the requested round number.
        """
        return self.images[round_number]

    def to_numpy_array(self) -> np.ndarray:
        """Method converting the whole tile to a numpy array.

        Returns:
            np.ndarray: the numpy array representation of a tile.
            It is of shape (rounds, channels, focus_levels, image_size, image_size).
        """
        tmp_list = []
        for image in self.images:
            tmp_list.append(image.get_data())
        return np.array(tmp_list)

    def get_channel(self, round: int, channel: int) -> np.ndarray:
        """Loads and returns the specified channel for all focus_levels.

        Args:
            round (int): The round to be returned
            channel (int): The channel to be returned

        Returns:
            np.ndarray: The loaded image of shape (focus_level, width, height)
        """

        return self.get_data()[channel, :, :, :]
        return self.images[round].get_channel(channel)

from situr.transformation.round_transformation import RoundTransform
import numpy as np

from situr.image.situ_image import SituImage
from situr.transformation import IdentityRoundTransform

from typing import List


class Tile:
    '''
    Rounds 5
    Channels 4+1 - spot colours + nuclei
    Z 1 to 30 - focus level
    Y 2048
    X 2048
    '''

    def __init__(self, file_list: List[List[List[str]]], nucleaus_channel: int = 4):
        self.images = []
        self.round_transformations = []
        for situ_image_list in file_list:
            self.images.append(
                SituImage(situ_image_list, nucleaus_channel=nucleaus_channel))
            self.round_transformations.append(IdentityRoundTransform())

    def apply_transformations(self):
        # first apply channel transformations then round transformations
        self.apply_channel_transformations()
        self.apply_round_transformations()

    def apply_channel_transformations(self):
        for i in range(self.get_round_count()):
            self.images[i].apply_transformations()

    def apply_round_transformations(self):
        for round, transformation in enumerate(self.round_transformations):
            transformation.apply_tranformation(self, round)

    def set_round_transformation(self, round, transformation: RoundTransform):
        self.round_transformations[round] = transformation

    def get_round_count(self) -> int:
        return len(self.images)

    def get_channel_count(self) -> int:
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
        tmp_list = []
        for image in self.images:
            tmp_list.append(image.get_data())
        return np.array(tmp_list)

    def get_channel(self, round: int, channel: int, focus_level: int = 0) -> np.ndarray:
        return self.images[round].get_channel(channel, focus_level=focus_level)

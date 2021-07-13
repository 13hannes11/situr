import numpy as np

from situr.image.situ_image import SituImage
from situr.transformation import IdentityRoundTransform


class Tile:
    '''
    Rounds 5
    Channels 4+1 - spot colours + nuclei
    Z 1 to 30 - focus level
    Y 2048
    X 2048
    '''

    def __init__(self, file_list, nucleaus_channel=4):
        self.images = []
        self.round_transformations = []
        for situ_image_list in file_list:
            self.images.append(
                SituImage(situ_image_list, nucleaus_channel=nucleaus_channel))
            self.round_transformations.append(IdentityRoundTransform())

    def apply_transformations():
        # TODO: implement (first apply channel transformations then round transformations)
        pass

    def get_image_round(self, round):
        return self.images[round]

    def set_round_transformation(self, round, transformation):
        self.round_transformations[round] = transformation

    def get_round_count(self):
        return len(self.images)

    def get_channel_count(self):
        return self.images[0].get_channel_count()

    def get_round(self, round_number):
        """This 

        Args:
            round_number (integer): The round number starting with 0

        Returns:
            SituImage: The image corresponding to the requested round number.
        """
        return self.images[id]

    def to_numpy_array(self):
        tmp_list = []
        for image in self.images:
            tmp_list.append(image.get_data())

        return np.array(tmp_list)

    def get_channel(self, round, channel, focus_level=0):
        return self.images[round].get_channel(channel, focus_level=focus_level)

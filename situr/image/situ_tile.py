import numpy as np

from situr.image.situ_image import SituImage


class Tile:
    '''
    * Rounds 5
    * Channels 4+1 - spot colours + nuclei
    * Z 1 to 30 - focus level
    * Y 2048
    * X 2048
    '''

    def __init__(self, file_list, nucleaus_channel=4):
        self.images = []
        for situ_image_list in file_list:
            self.images.append(
                SituImage(situ_image_list, nucleaus_channel=nucleaus_channel))

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

from situr.registration import Registration, FilterregRegistrationFunction
from situr.transformation import ScaleRotateTranslateRoundTransform


class RoundRegistration(Registration):
    def __init__(self, registration_function=FilterregRegistrationFunction(ScaleRotateTranslateRoundTransform)):
        super().__init__(registration_function)

    def do_round_registration(self, situ_tile, reference_round=0, reference_channel=0):
        """This method generates a round registration transformation for a tile and saves it in the tile. 

        Args:
            situ_tile (Tile): The tile that the transformation is to be performed on.
            reference_round (int, optional): The round that is referenced and will not be changed. Defaults to 0.
            reference_channel (int, optional): The channel tha is used to compare rounds. Defaults to 0.
        """

        # TODO: instead of one reference channel use all channels (maybe without nucleus channel)
        reference_peaks = situ_tile.get_image_round(
            reference_round).get_channel_peaks(reference_channel)
        for round in range(situ_tile.get_roundcount()):
            if round != reference_channel:
                current_round_peaks = situ_tile.get_image_round(
                    round
                ).get_channel_peaks(reference_channel)
                transformation = self.registration_function.do_registration(
                    current_round_peaks, reference_peaks)
                situ_tile.set_round_transformation(round, transformation)

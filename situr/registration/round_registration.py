from situr.image.situ_tile import Tile
import numpy as np

from situr.registration import Registration, RegistrationFunction, IcpRegistrationFunction


class RoundRegistration(Registration):

    def do_round_registration(self,
                              situ_tile,
                              reference_round: int = 0,
                              reference_channel: int = 0):
        """This method generates a round registration transformation for a tile
            and saves it in the tile.

        Args:
            situ_tile (Tile): The tile that the transformation is to be performed on.
            reference_round (int, optional): The round that is referenced and will not be changed.
                Defaults to 0.
            reference_channel (int, optional): The channel that is used to compare rounds.
                Defaults to 0.
        """

        reference_peaks = self.peak_finder.get_channel_peaks(situ_tile.get_round(
            reference_round), reference_channel)
        for round in range(situ_tile.get_round_count()):
            if round != reference_channel:
                current_round_peaks = self.peak_finder.get_channel_peaks(
                    situ_tile.get_round(round), reference_channel)
                transformation = self.registration_function.do_registration(
                    current_round_peaks, reference_peaks)
                situ_tile.set_round_transformation(round, transformation)


class AllChannelRoundRegistration(RoundRegistration):
    """This class perofrms a round registration using all channels instead of just the reference
        channel. It inherits from RoundRegistration.
    """

    def do_round_registration(self,
                              situ_tile: Tile,
                              reference_round: int = 0,
                              reference_channel: int = 0):
        """This method generates a round registration transformation for a tile and saves it in
            the tile.

        Args:
            situ_tile (Tile): The tile that the transformation is to be performed on.
            reference_round (int, optional): The round that is referenced and will not be changed.
                Defaults to 0.
            reference_channel (int, optional): This parameter is ignored.
        """
        reference_peaks = []
        for channel in range(situ_tile.get_channel_count()):
            # TODO: possibly exclude nucleaus channel
            reference_peaks.append(self.peak_finder.get_channel_peaks(situ_tile.get_round(
                reference_round), channel))
        reference_peaks = np.concatenate(reference_peaks, axis=0)

        for round in range(situ_tile.get_round_count()):
            if round != reference_channel:
                current_round_peaks = []
                for channel in range(situ_tile.get_channel_count()):
                    # TODO: possibly exclude nucleaus channel
                    current_round_peaks.append(self.peak_finder.get_channel_peaks(
                        situ_tile.get_round(round), channel))
                current_round_peaks = np.concatenate(
                    current_round_peaks, axis=0)

                transformation = self.registration_function.do_registration(
                    current_round_peaks, reference_peaks)
                situ_tile.set_round_transformation(round, transformation)

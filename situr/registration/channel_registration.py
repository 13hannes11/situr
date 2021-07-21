import numpy as np
from situr.image import situ_image

from situr.image.situ_tile import Tile
from situr.registration.peak_finder import PeakFinder, PeakFinderDifferenceOfGaussian
from situr.image.situ_image import SituImage
from situr.registration import Registration, RegistrationFunction, FilterregRegistrationFunction


class SituImageChannelRegistration(Registration):
    def do_channel_registration(self, situ_img: SituImage, reference_channel: int = 0):
        # For each channel (except nucleus) compute transform compared to reference_channel
        # Add Channel transformation to Channel
        reference_peaks = self.peak_finder.get_channel_peaks(
            situ_img, reference_channel)
        for channel in range(situ_img.get_channel_count()):
            if channel != situ_img.nucleaus_channel and channel != reference_channel:
                current_channel_peaks = self.peak_finder.get_channel_peaks(
                    situ_img, channel)
                transformation = self.registration_function.do_registration(
                    current_channel_peaks, reference_peaks)
                situ_img.set_channel_transformation(
                    channel, transformation)


class ChannelRegistration(Registration):
    def do_channel_registration(self, tile: Tile, reference_channel: int = 0):
        registration = SituImageChannelRegistration()
        # For each channel (except nucleus) compute transform compared to reference_channel
        # Add Channel transformation to Channel
        for round in range(tile.get_round_count()):
            situ_img = tile.get_round(round)
            registration.do_channel_registration(situ_img, reference_channel)


class AcrossRoundChannelRegistration(ChannelRegistration):
    def do_channel_registration(self, tile: Tile, reference_channel: int = 0):
        reference_peaks = []
        for round in range(tile.get_round_count()):
            reference_peaks.append(self.peak_finder.get_channel_peaks(
                tile.get_round(round), reference_channel))
        reference_peaks = np.concatenate(reference_peaks, axis=0)
        for channel in range(tile.get_channel_count()):
            if channel != tile.get_round(0).nucleaus_channel and channel != reference_channel:
                current_channel_peaks = []
                for round in range(tile.get_round_count()):
                    current_channel_peaks.append(
                        self.peak_finder.get_channel_peaks(tile.get_round(round), channel))
                current_channel_peaks = np.concatenate(
                    current_channel_peaks, axis=0)

                transformation = self.registration_function.do_registration(
                    current_channel_peaks, reference_peaks)
                for round in range(tile.get_round_count()):
                    tile.get_round(round).set_channel_transformation(
                        channel, transformation)

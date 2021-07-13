from situr.registration import Registration
from situr.transformation import IdentityChannelTransform


class ChannelRegistration(Registration):
    def do_channel_registration(self, situ_img, reference_channel=0):
        # For each channel (except nucleus) compute transform compared to reference_channel
        # Add Channel transformation to Channel
        reference_peaks = situ_img.get_channel_peaks(reference_channel)
        for channel in range(situ_img.get_channel_count()):
            if channel != situ_img.nucleaus_channel and channel != reference_channel:
                current_channel_peaks = situ_img.get_channel_peaks(channel)
                transformation = self.registration_function.do_registration(
                    current_channel_peaks, reference_peaks)
                situ_img.set_channel_transformation(channel, transformation)

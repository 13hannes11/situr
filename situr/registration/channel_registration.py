from situr.image.situ_image import SituImage
from situr.transformation.channel_transformation import ChannelTransform
from situr.registration import Registration, RegistrationFunction, FilterregRegistrationFunction
from situr.transformation import ChannelTransform, ScaleRotateTranslateChannelTransform


class ChannelRegistration(Registration):
    def __init__(self, registration_function: RegistrationFunction[ChannelTransform] = FilterregRegistrationFunction(ScaleRotateTranslateChannelTransform)):
        super().__init__(registration_function)

    def do_channel_registration(self, situ_img: SituImage, reference_channel: int = 0):
        # For each channel (except nucleus) compute transform compared to reference_channel
        # Add Channel transformation to Channel
        reference_peaks = situ_img.get_channel_peaks(reference_channel)
        for channel in range(situ_img.get_channel_count()):
            if channel != situ_img.nucleaus_channel and channel != reference_channel:
                current_channel_peaks = situ_img.get_channel_peaks(channel)
                transformation = self.registration_function.do_registration(
                    current_channel_peaks, reference_peaks)
                situ_img.set_channel_transformation(channel, transformation)

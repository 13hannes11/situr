import abc
import open3d as o3
from probreg import filterreg
from situr.image import extend_dim

from situr.transformation import ScaleRotateTranslateChannelTransform


class ChannelRegistration:
    __metaclass__ = abc.ABCMeta

    def do_registration(self, situ_img, reference_channel=0):
        # For each channel (except nucleus) compute transform compared to reference_channel
        # Add Channel transformation to Channel
        pass

    @abc.abstractmethod
    def register_single_channel(self, peaks_data, reference_peaks):
        """Performs the channel registration on an image. Expects the peaks in each image as input."""
        raise NotImplementedError(
            self.__class__.__name__ + '.register_single_channel')


class FilterregChannelRegistration(ChannelRegistration):
    def register_single_channel(self, data_peaks, reference_peaks):
        source = o3.geometry.PointCloud()
        source.points = o3.utility.Vector3dVector(extend_dim(data_peaks))
        target = o3.geometry.PointCloud()
        target.points = o3.utility.Vector3dVector(extend_dim(reference_peaks))

        registration_method = filterreg.registration_filterreg
        tf_param, _, _ = filterreg.registration_filterreg(source, target)

        return ScaleRotateTranslateChannelTransform(transform_matrix=tf_param.rot[0:2, 0:2], scale=tf_param.scale, offset=tf_param.t[0:2])

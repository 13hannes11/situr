import abc
from situr.registration.peak_finder import PeakFinderDifferenceOfGaussian
import open3d as o3
from probreg import filterreg
import numpy as np

from situr.image import extend_dim
from situr.transformation import Transform, ScaleRotateTranslateTransform


class RegistrationFunction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do_registration(self, data_peaks, reference_peaks) -> Transform:
        raise NotImplementedError(self.__class__.__name__ + '.do_registration')


class FilterregRegistrationFunction(RegistrationFunction):
    def do_registration(self, data_peaks: np.ndarray, reference_peaks: np.ndarray) -> ScaleRotateTranslateTransform:
        source = o3.geometry.PointCloud()
        source.points = o3.utility.Vector3dVector(extend_dim(data_peaks))
        target = o3.geometry.PointCloud()
        target.points = o3.utility.Vector3dVector(extend_dim(reference_peaks))

        registration_method = filterreg.registration_filterreg
        tf_param, _, _ = filterreg.registration_filterreg(source, target)

        return ScaleRotateTranslateTransform(transform_matrix=tf_param.rot[0:2, 0:2], scale=tf_param.scale, offset=tf_param.t[0:2])


class Registration:
    __metaclass__ = abc.ABCMeta

    def __init__(self, registration_function: RegistrationFunction() = FilterregRegistrationFunction(), peak_finder=PeakFinderDifferenceOfGaussian()):
        """Initialize channel registration and tell which registration function to use.

        Args:
            registration_function (RegistrationFunction, optional): Registration function. Defaults to FilterregRegistrationFunction(ScaleRotateTranslateChannelTransform).
            peak_finder (PeakFinder, optional): The peak finder to be used for the registration. Defaults to PeakFinderDifferenceOfGaussian().
        """
        self.registration_function = registration_function
        self.peak_finder = peak_finder

import abc
from situr.registration.peak_finder import PeakFinderDifferenceOfGaussian
import open3d as o3
from probreg import filterreg
import numpy as np

from situr.image import extend_dim
from situr.transformation import Transform, RotateTranslateTransform


class RegistrationFunction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do_registration(self, data_peaks: np.ndarray, reference_peaks: np.ndarray) -> Transform:
        """Method that does the registration on two arrays of peaks.

        Args:
            data_peaks (np.ndarray): [description]
            reference_peaks (np.ndarray): [description]

        Raises:
            NotImplementedError: This method is abstract and therefore calling
                it results in an error.

        Returns:
            Transform: The transformation that can be used to register data_peaks to the reference.
        """
        raise NotImplementedError(self.__class__.__name__ + '.do_registration')

class IcpRegistrationFunction(RegistrationFunction):
    def __init__(self, max_correspondence_distance=50) -> None:
        self.max_distance = max_correspondence_distance

    def do_registration(self,
                        data_peaks: np.ndarray,
                        reference_peaks: np.ndarray) -> RotateTranslateTransform:
        """Method that uses ICP to register the data_peaks.

        Args:
            data_peaks (np.ndarray): The peaks to be registered to the reference
            reference_peaks (np.ndarray): The reference peaks

        Returns:
            RotateTranslateTransform: the resulting transformaton from the registration
        """
        source = o3.geometry.PointCloud()
        source.points = o3.utility.Vector3dVector(extend_dim(data_peaks))
        target = o3.geometry.PointCloud()
        target.points = o3.utility.Vector3dVector(extend_dim(reference_peaks))
        reg_p2p = o3.pipelines.registration.registration_icp(
            source, target, self.max_distance)
        return RotateTranslateTransform(
            reg_p2p.transformation[0:2, 0:2],
            offset=reg_p2p.transformation[[1, 0], 3])


class Registration:
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 registration_function: RegistrationFunction() = IcpRegistrationFunction(),
                 peak_finder=PeakFinderDifferenceOfGaussian()):
        """Initialize channel registration and tell which registration function to use.

        Args:
            registration_function (RegistrationFunction, optional): Registration function.
                Defaults to IcpRegistrationFunction().
            peak_finder (PeakFinder, optional): The peak finder to be used for the registration.
                Defaults to PeakFinderDifferenceOfGaussian().
        """
        self.registration_function = registration_function
        self.peak_finder = peak_finder

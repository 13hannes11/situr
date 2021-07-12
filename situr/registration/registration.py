import abc
import open3d as o3
from probreg import filterreg

from situr.image import extend_dim
from situr.transformation import ScaleRotateTranslateChannelTransform


class RegistrationFunction:
    __metaclass__ = abc.ABCMeta

    def __init__(self, transormation_type=ScaleRotateTranslateChannelTransform):
        self.transormation_type = transormation_type

    @abc.abstractmethod
    def do_registration(self, data_peaks, reference_peaks):
        raise NotImplementedError(self.__class__.__name__ + '.do_registration')


class FilterregRegistrationFunction(RegistrationFunction):
    def do_registration(self, data_peaks, reference_peaks):
        source = o3.geometry.PointCloud()
        source.points = o3.utility.Vector3dVector(extend_dim(data_peaks))
        target = o3.geometry.PointCloud()
        target.points = o3.utility.Vector3dVector(extend_dim(reference_peaks))

        registration_method = filterreg.registration_filterreg
        tf_param, _, _ = filterreg.registration_filterreg(source, target)

        return self.transormation_type(transform_matrix=tf_param.rot[0:2, 0:2], scale=tf_param.scale, offset=tf_param.t[0:2])


class Registration:
    def __init__(self, registration_function):
        self.registration_function = registration_function

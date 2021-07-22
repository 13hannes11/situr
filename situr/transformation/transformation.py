import abc
import numpy as np
import scipy


class Transform:
    """Abstract class representing a transformatio that can be performed on an image.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply_tranformation(self, img: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            self.__class__.__name__ + '.apply_transformation')


class IdentityTransform(Transform):
    """A transformation that does not change the image.
        It inherits from Transform.
    """

    def apply_tranformation(self, img: np.ndarray) -> np.ndarray:
        return img


class ScaleRotateTranslateTransform(Transform):
    def __init__(self,
                 transform_matrix: np.ndarray,
                 scale: int = 1,
                 offset: np.array = np.array([0, 0])):
        """Constructor for a Transformation that supports rotation, translation and scaling on an
            image

        Args:
            transform_matrix (np.ndarray): A matrix of shape (2,2)
            scale (int, optional): The scale factor. Defaults to 1.
            offset (np.array, optional): The offset of shape (2,). Defaults to np.array([0, 0]).
        """
        # TODO: check
        #   * transform matrix is 2x2
        #   * offset is array (2,)
        self.transform_matrix = transform_matrix
        self.offset = offset
        self.scale = scale

    def apply_tranformation(self, img: np.ndarray) -> np.ndarray:
        img[:, :] = scipy.ndimage.affine_transform(
            img, self.transform_matrix)
        img[:, :] = scipy.ndimage.zoom(img, self.scale)
        img[:, :] = scipy.ndimage.shift(img, self.offset)

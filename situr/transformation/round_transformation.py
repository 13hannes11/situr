import abc
import scipy
import numpy as np
from situr.image import situ_image


class RoundTransform:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply_transformation(self, situ_tile, round):
        """Performs a transformation on one round, all channels and focus_levels are transformed the same way"""
        raise NotImplementedError(
            self.__class__.__name__ + '.apply_transformation')


class IdentityRoundTransform(RoundTransform):
    def apply_transformation(self, situ_tile, round):
        pass


class ScaleRotateTranslateRoundTransform(RoundTransform):
    def __init__(self, transform_matrix, scale=1, offset=np.array([0, 0])):
        # TODO: check
        #   * transform matrix is 2x2
        #   * offset is array (2,)
        self.transform_matrix = transform_matrix
        self.offset = offset
        self.scale = scale

    def apply_tranformation(self, situ_tile, round):
        situ_image = situ_tile.get_image_round(round)

        for channel in range(situ_image.get_channel_count()):
            for focus_level in range(situ_image.get_focus_level_count()):
                img = situ_image.get_focus_level(channel, focus_level)
                img[:, :] = scipy.ndimage.affine_transform(
                    img, self.transform_matrix)
                img[:, :] = scipy.ndimage.zoom(img, self.scale)
                img[:, :] = scipy.ndimage.shift(img, self.offset)

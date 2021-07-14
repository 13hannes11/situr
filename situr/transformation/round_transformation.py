import abc
from situr.image.situ_tile import Tile
import scipy
import numpy as np
from situr.image import situ_image
from situr.transformation import Transform


class RoundTransform(Transform):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply_transformation(self, situ_tile: Tile, round: int):
        """Performs a transformation on one round, all channels and focus_levels are transformed the same way

        Args:
            situ_tile (Tile): The tile the transformation is applied to.
            round (int): The round that the transformation is to be applied to.

        Raises:
            NotImplementedError: This method is abstract and therefore raises an error
        """
        raise NotImplementedError(
            self.__class__.__name__ + '.apply_transformation')


class IdentityRoundTransform(RoundTransform):
    def apply_transformation(self, situ_tile: Tile, round: Tile):
        """Performs the identity transformation (meaning no transformation)
        Args:
            situ_tile (Tile): The tile the transformation is applied to.
            round (Tile): The round that the transformation is to be applied to.
        """
        pass


class ScaleRotateTranslateRoundTransform(RoundTransform):
    def __init__(self, transform_matrix: np.ndarray, scale: int = 1, offset: np.array = np.array([0, 0])):
        """Constructor for a Transformation that supports rotation, translation and scaling on a channel

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

    def apply_tranformation(self, situ_tile: Tile, round: int):
        situ_image = situ_tile.get_image_round(round)

        for channel in range(situ_image.get_channel_count()):
            for focus_level in range(situ_image.get_focus_level_count()):
                img = situ_image.get_focus_level(channel, focus_level)
                img[:, :] = scipy.ndimage.affine_transform(
                    img, self.transform_matrix)
                img[:, :] = scipy.ndimage.zoom(img, self.scale)
                img[:, :] = scipy.ndimage.shift(img, self.offset)

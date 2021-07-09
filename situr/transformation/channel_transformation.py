class ChannelTransform:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply_transformation(self, situ_img , channel):
        """Performs a transformation on one channel, all focus_levels are transformed the same way"""
        raise NotImplementedError(self.__class__.__name__ + '.apply_transformation')


class ScaleRotateTranslateChannelTransform(ChannelTransform):
    def __init__(self, transform_matrix, scale=1, offset=np.array([0, 0])):
        # TODO: check 
        #   * transform matrix is 2x2
        #   * offset is array (2,)
        self.transform_matrix = transform_matrix
        self.offset = offset
        self.scale = scale

    def apply_tranformation(self, situ_img , channel):
        channel_img = situ_img.get_channel(channel)
        focus_levels = channel_img.shape[0]

        for focus_level in range(focus_levels):
            img = channel_img [focus_level, :, :]

            img [:, :] = scipy.ndimage.affine_transform(img, self.transform_matrix)
            img [:, :] = scipy.ndimage.zoom(img, self.scale)
            img [:, :] = scipy.ndimage.shift(img, self.offset)
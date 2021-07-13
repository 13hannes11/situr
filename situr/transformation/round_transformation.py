import abc


class RoundTransform:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply_transformation(self, situ_tile, channel):
        """Performs a transformation on one channel, all focus_levels are transformed the same way"""
        raise NotImplementedError(
            self.__class__.__name__ + '.apply_transformation')


class IdentityRoundTransform(RoundTransform):
    def apply_transformation(self, situ_tile, channel):
        pass

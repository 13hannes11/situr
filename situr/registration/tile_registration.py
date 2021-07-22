from situr.image.situ_tile import Tile
from situr.registration import RoundRegistration, ChannelRegistration, round_registration


class CombinedRegistration:
    """CombinedRegistration is a registration that performs a channel and a round transformaton
        after each other. Also the transformations are directly applied after each registration.
    """

    def __init__(self,
                 round_registration: RoundRegistration = RoundRegistration(),
                 channel_registration: ChannelRegistration = ChannelRegistration(),
                 reference_channel: int = 0,
                 reference_round: int = 0) -> None:
        self.round_registration = round_registration
        self.channel_registration = channel_registration
        self.reference_channel = reference_channel
        self.reference_round = reference_round

    def do_registration_and_transform(self, tile: Tile):
        """ This function applies the registration in the following order:
            1. Register the channels for each round of each tile.
            2. Apply transformations
            3. Register the rounds
            4. Apply transformation

        Args:
            tile (Tile): The tile that the registration and transformations are to be performed on.
        """
        self.channel_registration.do_channel_registration(
            tile, self.reference_channel)

        tile.apply_channel_transformations()

        self.round_registration.do_round_registration(tile,
                                                      self.reference_round,
                                                      self.reference_channel)

        tile.apply_round_transformations()

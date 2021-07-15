from situr.image.situ_tile import Tile
from situr.registration import RoundRegistration, ChannelRegistration, round_registration


class CombinedRegistration:
    def __init__(self, round_registration: RoundRegistration = RoundRegistration(), channel_registration: ChannelRegistration = ChannelRegistration(), reference_channel=0) -> None:
        self.round_registration = round_registration
        self.channel_registration = channel_registration

    def do_registration_and_transform(self, tile: Tile):
        """ This function applies the registration in the following order:
            1. Register the channels for each round of each tile.
            2. Apply transformations
            3. Register the rounds
            4. Apply transformation

        Args:
            tile (Tile): The tile that the registration and transformations are to be performed on.
        """
        # Do channel registration
        for round in range(tile.get_round_count()):
            img = tile.get_round(round)
            self.channel_registration

        tile.apply_channel_transformations()

        self.round_registration.do_round_registration(tile)

        tile.apply_round_transformations()

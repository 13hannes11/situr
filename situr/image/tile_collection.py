class TileCollection:
    '''
    The idea here is about a class that knows where to find all the images and then being able to load the tile that is wanted on demand.
    Therefore it also needs to know about the metadata.
    We need to keep track off transformatons for each channel and tile.

    * Tiles ~100
    * Rounds 5
    * Channels 4+1 - spot colours + nuclei
    * Z 1 to 30 - focus level
    * Y 2048
    * X 2048
    '''
    def __init__(self):
        pass
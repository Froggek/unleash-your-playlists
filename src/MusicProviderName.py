from enum import Enum, unique

@unique
class MusicProviderName(Enum): 
    DEEZER = 0
    SPOTIFY = 1
    YOUTUBE = 2
__title__ = 'connect4.py'
__author__ = 'airo.pi_'
__license__ = 'MIT'
__version__ = '1.0.3'

from .core import Connect4 as Connect4
from .core import Players as Players
from .errors import ColumnFull as ColumnFull
from .errors import GameOver as GameOver
from .errors import InvalidColumn as InvalidColumn

__all__ = ['Connect4', 'Players', 'ColumnFull', 'GameOver', 'InvalidColumn']

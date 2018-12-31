import os
from enum import Enum

DIR = os.path.dirname(os.path.realpath(__file__))
IMG_DIR = f'{DIR}/img'


class AssetsMapper(Enum):
    APP_ICON = f'{IMG_DIR}/icon.png'
    PINNED = f'{IMG_DIR}/pinned.png'
    PINNED_SELECTED = f'{IMG_DIR}/pinned_selected.png'

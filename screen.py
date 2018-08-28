import pygame as pg


class Screen:
    width  = 640
    height = 480

    def __init__(self):
        pg.font.init()

        self._frame = pg.display.set_mode((Screen.width, Screen.height), pg.DOUBLEBUF | pg.HWSURFACE)
        self._font  = pg.font.SysFont('Times New Roman', 30)

        pg.display.set_caption('snAIk')

    @property
    def frame(self):
        return self._frame

    @property
    def font(self):
        return self._font

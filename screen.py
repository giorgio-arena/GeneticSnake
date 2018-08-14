import pygame


class Screen:
    width  = 640
    height = 480

    def __init__(self):
        pygame.font.init()

        self._frame = pygame.display.set_mode((Screen.width, Screen.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self._font  = pygame.font.SysFont('Times New Roman', 30)

        pygame.display.set_caption('snAIk')

    @property
    def frame(self):
        return self._frame

    @property
    def font(self):
        return self._font

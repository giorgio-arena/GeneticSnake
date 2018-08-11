import pygame


class Screen:
    width  = 640
    height = 480

    def __init__(self):
        pygame.font.init()

        self.frame = pygame.display.set_mode((Screen.width, Screen.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.font  = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.display.set_caption('snAIk')

    def get_frame(self):
        return self.frame

    def get_font(self):
        return self.font

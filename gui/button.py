import pygame as pg


class Button:
    def __init__(self, btn_color, txt_color, rect, text):
        self._btn_color = btn_color
        self._txt_color = txt_color
        self._rect      = rect
        self._text      = text

    def draw(self, frame, font):
        pg.draw.rect(frame, self._btn_color, self._rect)
        text_surface = font.render(self._text, False, self._txt_color)
        frame.blit(text_surface, (self._rect[0] + self._rect[2] / 3, self._rect[1] + self._rect[3] / 3))

    def mouse_over(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)
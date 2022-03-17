import os
import pygame
import pygame as pg
from pygame.locals import *
from ext.eztext import Input as TextHolder

pg.init()
pg.font.init()
bg_color = (255, 204, 204)

title_font = pg.font.Font('./static/font/Aller_Bd.ttf', 14)
input_font = pg.font.Font('./static/font/Aller_BdIt.ttf', 14)

class InputPage:
   def __init__(self, name, size, title, title_font=title_font, input_font=input_font):
         self.done      = 0
         self.name      = name
         self.size      = size
         self.title     = title
         self.inp       = None
         self.surface   = None
         self.draw(title_font, input_font)


   def draw(self, title_font, input_font):

      # Program name
      pg.display.set_caption(self.name)

      # Draw dialog
      dialog_rect    = pg.Rect(self.size)
      self.surface   = pg.display.set_mode((dialog_rect.w, dialog_rect.h))
      self.surface.fill(bg_color)
      image = pygame.image.load(r'./static/img/pathfinder.png')
      image_small = pg.transform.scale(image, (700, 500))
      self.surface.blit(image_small, (50, 20))

      # Draw box outline
      outline_box_size = (180, 550, dialog_rect.w * 0.6, dialog_rect.h * 0.05)
      outline_box_rect = pg.Rect(outline_box_size)

      pg.draw.rect(self.surface, pg.Color('white'), outline_box_rect, 1)

      # Draw title
      title_box      = title_font.render(self.title, True, pg.Color('black'))
      title_rect     = title_box.get_rect()
      title_rect.x   = outline_box_rect.x + 8
      title_rect.y   = outline_box_rect.y - 22
      self.surface.blit(title_box, title_rect)

      # Draw input box
      inp_x, inp_y = outline_box_rect.x + 8, outline_box_rect.y + 6
      self.inp = TextHolder(x=inp_x, y=inp_y, maxlength=50, width=36, font=input_font, prompt=' ')
      self.inp.draw(self.surface)

      pg.display.update()


   def run(self):
      while self.done == 0:
         events = pg.event.get()
         self.inp.update(events)
         self.surface.fill(pg.Color('white'), self.inp.get_rect())
         self.inp.draw(self.surface)

         for e in events:
            if e.type == pg.QUIT:
               self.done = -1
            elif e.type == pg.KEYDOWN and e.key == K_RETURN:
               self.done = 1
         pg.display.flip()

      return (1, self.inp.get_text()) if self.done == 1 else (-1, None)


os.environ['SDL'] = '25012002'

# Run home screen to input file path
path_input = InputPage(name='Robot Path Finding', size=(0, 0, 800, 600), title='Map file:')
option, path = path_input.run()

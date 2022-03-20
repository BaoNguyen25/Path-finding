# Import pygame libraries
import pygame as pg
from pygame.locals import *

# Import search algorithms
from algo.bfs import bfs
from algo.dfs import dfs


# Import extensions
from ext.eztext import Input as TextHolder

FPS         = 20
clock       = pg.time.Clock()
font        = pg.font.Font('./static/font/Aller_Rg.ttf', 15)
font_bold   = pg.font.Font('./static/font/Aller_BdIt.ttf', 20)
font_title  = pg.font.Font('./static/font/LeagueSpartan-Bold.otf', 32)
color = (255, 204, 204)

class View:

   def __init__(self, view_map, grid, size):
      self.state = 0
      self.map = view_map
      self.size = size
      self.grid = grid
      self.search_names = []
      self.inp = None
      self.obstacle = None
      self.surface = None

   # Draw map on the surface
   def draw_map(self, movable=False):
      self.obstacle  = self.map.draw(surface=self.surface, grid=self.grid, movable=movable)


   def display(self):

      # Display window screen
      window_rect = pg.Rect(self.size)
      self.surface = pg.display.set_mode((window_rect.w * 40, window_rect.h * 35))
      self.surface.fill(color)

      # Draw map
      self.draw_map()

      # Display program name
      prog_text = 'ROBOT PATH FINDING'
      prog_box = font_title.render(prog_text, True, pg.Color('brown'))
      prog_rect = prog_box.get_rect()
      prog_rect.x = 300
      prog_rect.y = 40
      self.surface.blit(prog_box, prog_rect)

      # Display Start Node
      s_text = 'Blue: Source node'
      s_box = font_bold.render(s_text, True, pg.Color('steelblue'))
      s_rect = s_box.get_rect()
      s_rect.bottom = self.surface.get_rect().bottom
      s_rect.x = 30
      s_rect.y = 560
      self.surface.blit(s_box, s_rect)

      # Display Goal Node
      g_text = 'Red: Goal node'
      g_box = font_bold.render(g_text, True, pg.Color('tomato'))
      g_rect = g_box.get_rect()
      g_rect.bottom = self.surface.get_rect().bottom
      g_rect.x = 230
      g_rect.y = 560
      self.surface.blit(g_box, g_rect)

      # Display obstacles
      o_text = 'Orange: Obstacle'
      o_box = font_bold.render(o_text, True, pg.Color('orange'))
      o_rect = o_box.get_rect()
      o_rect.bottom = self.surface.get_rect().bottom
      o_rect.x = 390
      o_rect.y = 560
      self.surface.blit(o_box, o_rect)

      # Display path
      p_text = 'Green: Path from source to goal'
      p_box = font_bold.render(p_text, True, pg.Color('green3'))
      p_rect = p_box.get_rect()
      p_rect.bottom = self.surface.get_rect().bottom
      p_rect.x = 570
      p_rect.y = 560
      self.surface.blit(p_box, p_rect)

      # Display title
      title_text = 'Search algorithms:'
      title_box = font_bold.render(title_text, True, pg.Color('black'))
      title_rect = title_box.get_rect()
      title_rect.bottom = self.surface.get_rect().bottom
      title_rect.x = 20
      title_rect.y = 200
      self.surface.blit(title_box, title_rect)

      # Display options for algorithms
      prev_y = title_rect.y + 8
      self.search_names      = ['Bread-First Search', 'Depth-First Search']

      for idx, e in enumerate(self.search_names):
         opt_box = font.render('{}. {}'.format(idx + 1, e), True, pg.Color('black'))
         opt_rect = opt_box.get_rect()
         opt_rect.x = title_rect.x + 8
         opt_rect.y = prev_y + 20
         prev_y = opt_rect.y
         self.surface.blit(opt_box, opt_rect)

      # Display input box
      outline_box_size = (title_rect.x, prev_y + 30, 200, 25)
      outline_box_rect = pg.Rect(outline_box_size)
      pg.draw.rect(self.surface, pg.Color('white'), outline_box_rect, 1)

      inp_x, inp_y = outline_box_rect.x + 4, outline_box_rect.y + 4
      self.inp = TextHolder(x=inp_x, y=inp_y, maxlength=1, width=15, font=font, restricted='12', prompt=' Enter choice: ')
      self.inp.draw(self.surface)

      # Update changes
      pg.display.update(self.surface.get_rect())

   def find_path(self, algorithm):
      self.draw_map()
      pg.display.update(self.surface.get_rect())
      target_found, cost, path = False, -1, None
      print('-> Running {}:'.format(algorithm))

      if algorithm == 'Bread-First Search':
         target_found, cost, path = bfs(s=self.map.S, g=self.map.G, w=self.map.border.w, h=self.map.border.h, limited=self.obstacle)
      elif algorithm == 'Depth-First Search':
         target_found, cost, path = dfs(s=self.map.S, g=self.map.G, w=self.map.border.w, h=self.map.border.h, limited=self.obstacle)

      self.display_path(target_found, cost, path, pg.Color('green3'))

   def display_path(self, target_found, cost, path, color):
      if not target_found:
         print('No path found')
         return

      print('Finding...')

      for e in path:
         self.surface.fill(color, self.grid[e.y][e.x])
         pg.display.update(self.grid[e.y][e.x])
         clock.tick(FPS)

      print('Target found')
      print('Cost: {0:.2f}'.format(cost))

   def run(self):
      self.display()

      while self.state == 0:
         events = pg.event.get()

         # Update user input
         self.inp.update(events)
         self.surface.fill(pg.Color('white'), self.inp.get_rect())
         self.inp.draw(self.surface)

         for e in events:

            # User clicks exit button
            if e.type == pg.QUIT:
               self.state = 1
               continue

            # If user hits ENTER
            if e.type == pg.KEYDOWN and e.key == K_RETURN:

               # User input text
               if self.inp.get_text() != '':
                  algorithm_idx = int(self.inp.get_text())
                  self.find_path(self.search_names[algorithm_idx - 1])

               self.inp.reset_text()
               self.surface.fill(pg.Color('white'), self.inp.get_rect())
               self.inp.draw(self.surface)

         pg.display.flip()

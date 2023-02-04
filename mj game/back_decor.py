import pygame
from settings1 import *
from Tiles import AnimatedTile,StaticTile
from support import import_folder
from random import choice,randint

class Sky:
     
     def __init__(self,horizon,style = 'level'):
          self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
          self.mid = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
          self.bot = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
          self.horizon = horizon

          # stretchin part
          self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
          self.mid = pygame.transform.scale(self.mid,(screen_width,tile_size))
          self.bot = pygame.transform.scale(self.bot,(screen_width,tile_size))
          self.style = style
          if self.style == 'overworld':
               tree_surface = import_folder()
     def draw(self,surface):
          for row in range(vertical_tile_number):
               y = row * tile_size
               if row < self.horizon:
                    surface.blit(self.top,(0,y))
               elif row == self.horizon:
                    surface.blit(self.mid,(0,y))
               else:
                    surface.blit(self.bot,(0,y))

class Water:

     def __init__(self,top,level_width) -> None:
          water_start = -screen_width
          water_tile_width = 192
          tile_x_amount = int((level_width + screen_width) / water_tile_width)+screen_width
          self.water_sprites = pygame.sprite.Group()

          for tile in range(tile_x_amount):
               x = tile * water_tile_width + water_start
               y = top
               sprite = AnimatedTile(192,x,y,('../graphics/decoration/water'))
               self.water_sprites.add(sprite)

     def draw(self,surface,shift):
          self.water_sprites.update(shift)
          self.water_sprites.draw(surface)

class Clouds:
     def __init__(self,horizon,level_width,cloud_number) -> None:
          cloud_surf_list = import_folder('../graphics/decoration/clouds')
          min_x = -screen_width
          max_x = level_width+screen_width
          min_y = 0
          max_y = horizon
          self.cloud_sprites = pygame.sprite.Group()

          for cloud in range(cloud_number):
               cloud = choice(cloud_surf_list)
               x = randint(min_x,max_x)
               y = randint(min_y,max_y)

               sprite = StaticTile(0,x,y,cloud)
               self.cloud_sprites.add(sprite)

     def draw(self,surface,shift):
          self.cloud_sprites.update(shift)
          self.cloud_sprites.draw(surface)
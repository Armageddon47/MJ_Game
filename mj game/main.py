import pygame, sys
from level import Level
from settings1 import *
from Game_data import *
from Overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        #game atts
        self.max_level = 5
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        #audio
        self.level_music= pygame.mixer.Sound('../graphics/sounds/main.mp3')
        self.level_music.set_volume(0.5)
        self.overworld_music= pygame.mixer.Sound('../graphics/sounds/overworld.mp3')
        self.overworld_music.set_volume(0.3)

        #overworld
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_music.play(loops = -1)
        self.level_music.stop()

        #user interface
        self.ui = UI(screen)

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_music.stop()
        self.level_music.play()

    def create_overworld(self,current_level,new_max_level):
        if new_max_level>self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        if self.level_music:
            self.level_music.stop()
        self.overworld_music.play()

    def change_coins(self,amount):
        self.coins += amount

    def change_health(self,amount):
        self.cur_health+= amount
      
    def check_gameover(self):

        if self.cur_health<=0:
            self.cur_health=100
            self.create_overworld(self.max_level, 0)
            self.level_music.stop()
            self.overworld_music.play()
            
    def run (self):
        if self.status=='overworld':
            self.overworld.run()
            

        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_gameover()
            


pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()
    
    pygame.display.update()
    clock.tick(60)

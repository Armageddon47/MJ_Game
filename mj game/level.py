import pygame
from support import *
from settings1 import *
from Tiles import Tile, StaticTile, Coin,Palm
from Game_data import levels
from enemy import Enemy
from back_decor import *
from Player import Player
from Particles import ParticleEffect

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
        #general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        #overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)

        #user interface
        self.change_coins = change_coins

        #audio
        self.coin_sound = pygame.mixer.Sound('../graphics/sounds/effects/coin.mp3')
        self.stomp_sound = pygame.mixer.Sound('../graphics/sounds/effects/hit.mp3')
        self.coin_sound.set_volume(0.25)
        #dust
        self.dust_sprites = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        #explosion
        self.explosion_sprites = pygame.sprite.Group()

        # trees
        fg_palm_layout = import_csv_layout(level_data['decor'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'decor')

        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		#constr
        constraint_layout = import_csv_layout(level_data['str'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'str')

        #background decor
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20,level_width)
        self.clouds = Clouds(400,level_width,30)
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size   
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../levels/ff1Copy.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size,x,y,'../graphics/coins/Gold',10)
                        if val == '1':
                            sprite = Coin(tile_size,x,y,'../graphics/coins/Silver',1)
                    if type == 'decor':
                        sprite = Palm(tile_size,x,y,'../graphics/decoration/trees')
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'str':
                        sprite = Tile(tile_size,x,y)
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self,layout,change_health):
         for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size 

                if val == '0':
                     sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                     self.player.add(sprite)
                if val == '1':
                    door_surface = pygame.image.load('../graphics/character/door.png').convert_alpha()

                    sprite = StaticTile(tile_size,x,y,door_surface)
                    self.goal.add(sprite)


    def enemy_col_reverse(self):
        for enemy in self.enemy_sprites:
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)

        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def horiz_movement_col(self): 
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed


        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 :
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <=0):
            player.on_right = False

    def vertical_movement_col(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0 :
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        
        if player.on_ground and player.direction.y <0 or player.direction.y >1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y >0:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width/4 and direction_x <0 :
            self.world_shift = 8
            player.speed = 0
        elif player_x>screen_width-(screen_width/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed =8
         
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprites.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)

            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprites.add(fall_dust_particle)

    def check_collided_coins(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)


    def check_enemy_collision(self):
         enemy_col = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

         if enemy_col:
            for enemy in enemy_col:
                enemy_center = enemy.rect.centery
                enemy_top =enemy.rect.top
                player_bot = self.player.sprite.rect.bottom
                if enemy_top < player_bot < enemy_center and self.player.sprite.direction.y >=0:
                    self.player.sprite.direction.y =- 15
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                    self.stomp_sound.play()
                else:                                
                    self.player.sprite.get_damage()

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
           self.create_overworld(self.current_level, 0)
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
              self.create_overworld(self.current_level, self.new_max_level)           
    def run(self):
        # run entire

        #back decor
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw((self.display_surface))

        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        self.check_collided_coins()

        #dust particle
        self.dust_sprites.update(self.world_shift)
        self.dust_sprites.draw(self.display_surface)
        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_col_reverse()
        self.constraint_sprites.update(self.world_shift)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        #trees
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #player sprites
        self.player.update()
        self.horiz_movement_col()
        self.get_player_on_ground()
        self.vertical_movement_col()
        self.create_landing_dust()

       # self.vertical_movement_col()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.scroll_x()

        self.check_death()
        self.check_win()
        self.check_enemy_collision()

        #water
        self.water.draw(self.display_surface,self.world_shift)
import pygame 

class UI:
     def __init__(self,surface) -> None:
          
          self.display_surface = surface

          #health
          self.health_bar100 = pygame.image.load('../graphics/ui/health_100.png').convert_alpha()
          self.health_bar75 = pygame.image.load('../graphics/ui/health_75.png').convert_alpha()
          self.health_bar50 = pygame.image.load('../graphics/ui/health_50.png').convert_alpha()
          self.health_bar25 = pygame.image.load('../graphics/ui/health_25.png').convert_alpha()
          self.health_bar0 = pygame.image.load('../graphics/ui/health_0.png').convert_alpha()

          self.health_bar_topleft = (54,39)
          self.bar_max_width = 148
          self.bar_height = 8

          #coins
          self.coins = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
          self.coin_rect = self.coins.get_rect(topleft = (50,60))
          self.font = pygame.font.Font('../graphics/ui/Candara.ttf',30)

     def show_health(self,current,max):
          current_health_rate = current/max
          health_disp = current_health_rate
          if current_health_rate <=0:
               health_disp = self.health_bar0
          elif current_health_rate < 0.26:
               health_disp = self.health_bar25
          elif current_health_rate < 0.51:
               health_disp= self.health_bar50
          elif current_health_rate < 0.76:
              health_disp= self.health_bar75
          elif current_health_rate > 0.76:     
               health_disp= self.health_bar100
          self.display_surface.blit(health_disp,(20,10))
          #current_health_width = self.bar_max_width * current_health_rate
         # hearlth_bar_rect = pygame.Rect(self.health_bar_topleft,(current_health_width,self.bar_height))
          #pygame.draw.rect(self.display_surface,'#000000',hearlth_bar_rect)


     def show_coins(self,amount):
          self.display_surface.blit(self.coins,self.coin_rect)
          coin_amount_surf=self.font.render(str(amount),False,'#d95726')
          coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
          self.display_surface.blit(coin_amount_surf,coin_amount_rect)
import pygame
import constantes as c


class Weapons():
    
    def __init__(self,animations_w):

        self.frame_index=0
        self.animations_w = animations_w
        self.image = animations_w[self.frame_index]
        self.shape = self.image.get_rect()
        self.update_time = pygame.time.get_ticks()

        

    def update(self, player):
        cooldown_animation = 500
        self.shape.center = player.shape.center

        if player.flip:
            self.shape.x -= player.shape.width//2.2
            self.rotate_weapon(False)
        else:
            self.shape.x += player.shape.width//2.2
            self.rotate_weapon(True)

        self.image = self.animations_w[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animation:
                 
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animations_w):

            self.frame_index = 0            




    def draw(self, interfaz):
        interfaz.blit(self.image, self.shape) 
        #pygame.draw.rect(interfaz, c.p_color,self.shape,1)       


    def rotate_weapon(self,rotar):
        
        if rotar==True:
            self.image = pygame.transform.flip(self.image,True,False)


        else:
            self.image = pygame.transform.flip(self.image,False,False)

     

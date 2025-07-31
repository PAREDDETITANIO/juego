import pygame
import constantes as c
import random as r

class Player():
    def __init__(self,x,y,animations):
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x,y)
        self.in_combat = False

    def update(self):
        if not self.in_combat:  # Solo actualizar animación si no está en combate
            cooldown_animation = 100
            self.image = self.animations[self.frame_index]

            if pygame.time.get_ticks() - self.update_time > cooldown_animation:     
                self.frame_index +=1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animations):
                self.frame_index = 0

    def draw(self,interfaz):   
        image_flip=pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(image_flip,self.shape)

    def move(self,dx,dy):
        if not self.in_combat:  # Solo mover si no está en combate
            if dx > 0:
                self.flip=False
            elif dx <0:
                self.flip=True

            self.shape.x +=dx 
            self.shape.y +=dy 
            self.shape.x = max(0,min(self.shape.x, c.ancho-self.shape.width))
            self.shape.y = max(0,min(self.shape.y, c.alto-self.shape.width))

class Enemy(Player):
    def __init__(self, x, y, animations):
        super().__init__(x, y, animations)
        self.speed = 1
        self.detection_radius = 500
        self.dx = 0
        self.dy = 0
        self.state = "idle"
        
    def update(self, player):
        if not player.in_combat:  # Solo actualizar si el jugador no está en combate
            distance_to_player = ((player.shape.x - self.shape.x)**2 + 
                                (player.shape.y - self.shape.y)**2)**0.5
            
            if distance_to_player < self.detection_radius:
                self.state = "chasing"
                # Moverse hacia el jugador
                dx = player.shape.x - self.shape.x
                dy = player.shape.y - self.shape.y
                dist = max(1, (dx**2 + dy**2)**0.5)
                self.dx = (dx/dist) * self.speed
                self.dy = (dy/dist) * self.speed
            else:
                self.state = "idle"
                # Movimiento aleatorio
                if r.random() < 0.02:
                    self.dx = r.choice([-1, 0, 1]) * self.speed
                    self.dy = r.choice([-1, 0, 1]) * self.speed
            
            # Actualizar posición
            self.shape.x += self.dx
            self.shape.y += self.dy
            
            # Actualizar animación
            super().update()
            
            # Comprobar colisión con el jugador
            if self.shape.colliderect(player.shape) and not player.in_combat:
                player.in_combat = True
                return True  # Indica que se inició combate
        return False
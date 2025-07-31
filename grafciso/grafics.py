import pygame
import constantes as c
import personaje as p
import weapons as w
import os

# Funciones auxiliares
def scal_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))

def cont_elem(carpeta):
    return len(os.listdir(carpeta))

def name_dir(carpeta):
    return os.listdir(carpeta)

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((c.ancho, c.alto))
pygame.display.set_caption("mi juego")
font = pygame.font.SysFont(None, 36)  # Fuente para texto

# Cargar animaciones del jugador
animations = []
for i in range(8):
    img = pygame.image.load(f"C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/character/player/sprite_{i}.png")
    animations.append(scal_img(img, c.scala_p))

# Cargar animaciones de armas
animations_w = []
for i in range(10):
    image_sword = pygame.image.load(f"C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/weapons/sprite_{i}.png")
    animations_w.append(scal_img(image_sword, c.scala_w))

# Cargar animaciones de enemigos
animations_e = []
enemis = "C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/character/enemi"
for eni in name_dir(enemis):
    list_tep = []
    ruta = f"C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/character/enemi/{eni}"
    for i in range(cont_elem(ruta)):
        image_enemi = pygame.image.load(f"{ruta}/sprite_{i}.png")
        list_tep.append(scal_img(image_enemi, c.scala_p))
    animations_e.append(list_tep)

# Crear personajes y objetos
jugador = p.Player(50, 50, animations)
sword = w.Weapons(animations_w)
enemigo = p.Enemy(300, 200, animations_e[0])

# Estados del juego
game_state = "exploration"  # "exploration" o "combat"
combat_background = pygame.Surface((c.ancho, c.alto))
combat_background.fill((50, 50, 80))  # Color azul oscuro para el combate

# Variables de movimiento
move_up = move_down = move_left = move_right = False
run = True
clock = pygame.time.Clock()

while run:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if game_state == "exploration":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: move_up = True
                if event.key == pygame.K_s: move_down = True
                if event.key == pygame.K_d: move_right = True
                if event.key == pygame.K_a: move_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w: move_up = False
                if event.key == pygame.K_s: move_down = False
                if event.key == pygame.K_d: move_right = False
                if event.key == pygame.K_a: move_left = False
        
        elif game_state == "combat" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "exploration"
                jugador.in_combat = False

    # Lógica del juego según el estado
    if game_state == "exploration":
        screen.fill(c.screan_color)
        
        # Movimiento del jugador
        dx, dy = 0, 0
        if move_up: dy -= c.speed
        if move_down: dy += c.speed
        if move_left: dx -= c.speed
        if move_right: dx += c.speed
        
        jugador.move(dx, dy)
        
        # Actualizar y dibujar elementos
        jugador.update()
        sword.update(jugador)
        
        # Comprobar si el enemigo inició combate
        if enemigo.update(jugador):
            game_state = "combat"
            # Guardar posición antes del combate
            pre_combat_pos = (jugador.shape.x, jugador.shape.y)
        
        enemigo.draw(screen)
        jugador.draw(screen)
        sword.draw(screen)
    
    elif game_state == "combat":

        jugador.frame_index = (jugador.frame_index + 1) % len(jugador.animations)
        enemigo.frame_index = (enemigo.frame_index + 1) % len(enemigo.animations)
        # Dibujar pantalla de combate
        screen.blit(combat_background, (0, 0))
        
        # Posiciones de combate
        player_pos = (c.ancho *0.1, -50+(c.alto // 2))
        enemy_pos = (c.ancho *0.7, -50+(c.alto // 2))
        
        # Dibujar personajes (escalados para el combate)
        player_img = pygame.transform.scale(
            pygame.transform.flip(jugador.animations[jugador.frame_index], False, False),
            (150, 150)
        )
        enemy_img = pygame.transform.scale(
            pygame.transform.flip(enemigo.animations[enemigo.frame_index], True, False),
            (150, 150)
        )
        
        screen.blit(player_img, player_pos)
        screen.blit(enemy_img, enemy_pos)
        
        # Dibujar texto de combate
        text = font.render("COMBATE! Presiona ESC para huir", True, (255, 255, 255))
        screen.blit(text, (c.ancho // 2 - text.get_width() // 2, 50))

        lugar=480
        font = pygame.font.Font(None, 24)
        text2 = font.render("1. Atacar", True, (255, 255, 255))
        screen.blit(text2, (c.ancho // 3.5 - text.get_width() // 2, lugar))
        text3 = font.render("2. Curar", True, (255, 255, 255))
        screen.blit(text3, (c.ancho // 3.5 - text.get_width() // 2, lugar+24))
        text3 = font.render("3. Inventario", True, (255, 255, 255))
        screen.blit(text3, (c.ancho // 3.5 - text.get_width() // 2, lugar+24*2))
        text4 = font.render("4. Stats", True, (255, 255, 255))
        screen.blit(text4, (c.ancho // 3.5 - text.get_width() // 2, lugar+24*3))
        clock.tick(c.FPS*0.2)


    pygame.display.update()
    clock.tick(c.FPS)

pygame.quit()
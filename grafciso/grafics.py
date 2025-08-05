import pygame
import constantes as c
import personaje as p
import weapons as w
import os
import random as r

# Funciones auxiliares
def scal_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))

def cont_elem(carpeta):
    return len(os.listdir(carpeta))

def name_dir(carpeta):
    return os.listdir(carpeta)


#texto

def dibujar_texto(texto, x, y, fuente, color=(255, 255, 255)):
    superficie = fuente.render(texto, True, color)
    screen.blit(superficie, (x, y))

def menu_turno_visual(fuente):
    dibujar_texto("1. Atacar", 50, lugar, fuente)
    dibujar_texto("2. Curar", 50, lugar+24, fuente)
    dibujar_texto("3. Inventario", 50, lugar+24*2, fuente)
    dibujar_texto("4. Stats", 50, lugar+24*3, fuente)

def menu_atac_visual(fuente):
    dibujar_texto("1. Básico", 150, lugar, fuente)
    dibujar_texto("2. Habilidad 1", 150, lugar+24, fuente)
    dibujar_texto("3. Habilidad 2", 150, lugar+24*2, fuente)
    dibujar_texto("4. Ultimate", 150, lugar+24*3, fuente)

def menu_inv_visual(fuente):
    dibujar_texto("1. Ver inventario", 50, 50, fuente)
    dibujar_texto("2. Cambiar arma", 50, 100, fuente)
    dibujar_texto("3. Cambiar armadura", 50, 150, fuente)

def menu_clase_visual(fuente):
    dibujar_texto("Elige tu clase:", 50, 30, fuente)
    dibujar_texto("1. Guerrero", 50, 80, fuente)
    dibujar_texto("2. Mago", 50, 130, fuente)
    dibujar_texto("3. Templario", 50, 180, fuente)
    dibujar_texto("4. Científico", 50, 230, fuente)
    dibujar_texto("5. Samurai", 50, 280, fuente)

def levelear_enemigo(enemigo, piso_actual):
    incremento = max(1, int(r.gauss(0 + piso_actual*0.5, 3)))  
    incremento = min(10 + piso_actual, incremento)
    for _ in range(incremento - 1):
        enemigo.levelup()

def seleccionar_clase():
    while True:
        name=input("Elije Un Nombre:")
        menu_clase_visual()
        entrada = input("Opción: ")
        print(f" Has ingresado: {entrada}")  
        
        try:
            opcion = int(entrada)
            if 1 <= opcion <= 5:
                return [p.Guerrero, p.Mago, p.Templario, p.Cientifico, p.Samurai][opcion-1](name)
            print("Error: Debe ser entre 1 y 5")
        except ValueError:
            print("Error: Debes ingresar SOLO números (1-5)")        

def seleccionar_clase_visual(screen, font, animations):
    clases = [
        ("Guerrero", "Fuerza bruta y defensa"),
        ("Mago", "Poder mágico y hechizos"),
        ("Templario", "Equilibrado y sagrado"),
        ("Cientifico", "Tecnología y inteligencia"),
        ("Samurai", "Precisión y velocidad")
    ]

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    HIGHLIGHT = (200, 150, 50)
    title_font = pygame.font.SysFont(None, 48)
    option_font = pygame.font.SysFont(None, 36)
    desc_font = pygame.font.SysFont(None, 24)

    nombre = ""
    input_active = True
    selected = 0
    running = True

    while running:
        screen.fill(BLACK)
        
        # Título
        title = title_font.render("SELECCIONA TU CLASE", True, WHITE)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))
        
        # Input para nombre
        name_label = option_font.render("Nombre del personaje:", True, WHITE)
        screen.blit(name_label, (screen.get_width()//2 - name_label.get_width()//2, 120))
        
        name_text = option_font.render(nombre, True, WHITE)
        pygame.draw.rect(screen, WHITE if input_active else GRAY, 
                        (screen.get_width()//2 - 150, 160, 300, 40), 2)
        screen.blit(name_text, (screen.get_width()//2 - name_text.get_width()//2, 165))
        
        # Opciones de clase
        for i, (clase, desc) in enumerate(clases):
            y_pos = 240 + i * 60
            color = HIGHLIGHT if i == selected else WHITE
            
            clase_text = option_font.render(f"{i+1}. {clase}", True, color)
            screen.blit(clase_text, (screen.get_width()//2 - clase_text.get_width()//2, y_pos))
            
            desc_text = desc_font.render(desc, True, WHITE)
            screen.blit(desc_text, (screen.get_width()//2 - desc_text.get_width()//2, y_pos + 35))
        
        # Instrucciones
        instrucciones = desc_font.render("Usa las flechas para navegar, ENTER para seleccionar", True, WHITE)
        screen.blit(instrucciones, (screen.get_width()//2 - instrucciones.get_width()//2, screen.get_height() - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += event.unicode
                else:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(clases)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(clases)
                    elif event.key == pygame.K_RETURN and nombre:
                        # Retorna la instancia del personaje seleccionado
                        clases_disponibles = [p.Guerrero, p.Mago, p.Templario, p.Cientifico, p.Samurai]
                        return clases_disponibles[selected](50, 50, animations,screen, nombre)
                    elif event.key == pygame.K_ESCAPE:
                        input_active = True
    
    return None





# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((c.ancho, c.alto))
pygame.display.set_caption("mi juego")

font = pygame.font.SysFont(None, 36)  # Fuente para texto
small_font = pygame.font.Font(None, 24)  # Fuente más pequeña para opciones

#fondo de combate
background = pygame.image.load("C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/fondos/fondo_1.png").convert()
# Escalar la imagen al tamaño de la pantalla
background = pygame.transform.scale(background, ( c.ancho, c.alto))

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
jugador = seleccionar_clase_visual(screen, font, animations)
if not jugador:  # Si el usuario cierra la ventana durante selección
    pygame.quit()
    exit()

#sword = w.Weapons(animations_w)
enemigo = p.Enemy(300, 200, animations_e[0],screen)

# Estados del juego
game_state = "exploration"  # "exploration" o "combat"
combat_background = pygame.Surface((c.ancho, c.alto))
combat_background.fill((50, 50, 80))  # Color azul oscuro para el combate



atac_act=False
damage_act=False

turno=1
# Variables de movimiento
move_up = move_down = move_left = move_right = False
run = True
clock = pygame.time.Clock()
end=False
exp_ga=0
exp_re=0
deamage_valu=0

while run:
    # Manejo de eventos (unificado para ambos estados)
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
            
            move_up = move_down = move_left = move_right = False

            if event.key == pygame.K_ESCAPE:
                game_state = "exploration"
                jugador.in_combat = False

            elif event.key == pygame.K_1:  # Atacar
                damage_act=  True
                if atac_act and event.key == pygame.K_1 :  
                    damage_act=  True

                    if jugador.velocidad_total() > enemigo.velocidad_total():
                        jugador.ataque(enemigo)
                        deamage_valu = jugador.damage(enemigo)
                        enemigo.ataque(jugador)
                    else:    
                        enemigo.ataque(jugador)
                        jugador.ataque(enemigo)
                        deamage_valu = jugador.damage(enemigo)
                    
                        

                    atac_act = False  
                
                elif event.key == pygame.K_2:
                    pass
                elif event.key == pygame.K_3:
                    pass 
                elif event.key == pygame.K_4:
                    pass
                else:
                    atac_act = True

                if not enemigo.vivo():
                    turno += 1
                    jugador.in_combat = False
                    exp_ga, exp_re = jugador.expc(enemigo.lvl)
                    end=True
                    game_state = "combat_end"


                                        

                if not jugador.vivo():    
                        game_state="game over"


            elif event.key == pygame.K_2 and not damage_act:  # Curar
                jugador.vida += 50
            elif event.key == pygame.K_3 and not damage_act:
                game_state = "inventario"
            elif event.key == pygame.K_4 and not damage_act:    
                mostrar_stats = True
            
                # Sub-bucle para mantener los stats visibles
                waiting_for_key = True

                while waiting_for_key:
                    # Dibujar todo (personajes, fondo, etc.)
                    screen.fill((64, 64, 64))
                    
                    jugador.draw(screen)
                    enemigo.draw(screen)
                    

                    # Dibujar atributos (encima de todo)
                    enemigo.mostrar_atributos(screen)
                    jugador.mostrar_atributos(screen)
                    
                    pygame.display.flip()
                    
                    # Esperar cualquier tecla para salir
                    for sub_event in pygame.event.get():
                        if sub_event.type == pygame.QUIT:
                            waiting_for_key = False
                            run = False
                        elif sub_event.type == pygame.KEYDOWN:  # Cualquier tecla cierra
                            waiting_for_key = False
                
                mostrar_stats = False

        elif game_state == "combat_end":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:  # También puedes usar pygame.K_SPACE
                        # Reiniciar combate
                        
                        enemigo = p.Enemy(300, 200, animations_e[0], screen)
                        levelear_enemigo(enemigo, turno)
                        game_state = "exploration"
                        enemigo.shape.x, enemigo.shape.y = 500, 500
                        jugador.shape.x, jugador.shape.y = 20, 20
                        end = damage_act = atac_act = False
                        











    # Lógica del juego según el estado
    if game_state == "exploration":
        screen.fill(c.screan_color)
        

        # Dibujar turno
        text = font.render(f"TURNO: {turno}", True, (255, 255, 255))
        screen.blit(text, (c.ancho // 2 - text.get_width() // 2, 50))


        # Movimiento del jugador
        dx, dy = 0, 0
        if move_up: dy -= c.speed
        if move_down: dy += c.speed
        if move_left: dx -= c.speed
        if move_right: dx += c.speed
        
        jugador.move(dx, dy)
        
        # Actualizar y dibujar elementos
        jugador.update()
        jugador.equipo["arma"].update(jugador)
        
        # Comprobar si el enemigo inició combate
        if enemigo.update(jugador):
            game_state = "combat"
            # Guardar posición antes del combate
            pre_combat_pos = (jugador.shape.x, jugador.shape.y)
        
        enemigo.draw(screen)
        jugador.draw(screen)
        jugador.equipo["arma"].draw(screen)
    
    elif game_state == "combat":
        # Actualizar animaciones
        jugador.frame_index = (jugador.frame_index + 1) % len(jugador.animations)
        enemigo.frame_index = (enemigo.frame_index + 1) % len(enemigo.animations)
        
        # Dibujar pantalla de combate
        screen.blit(background, (0, 0))
        

        # Escalado de tamaño
        altura_pixeles = jugador.altura * c.RELACION_CM_A_PIXEL
        ancho_pixeles = jugador.peso * c.RELACION_KG_A_PIXEL

        altura_pixeles_enemigo = enemigo.altura * c.RELACION_CM_A_PIXEL
        ancho_pixeles_enemigo = enemigo.peso * c.RELACION_KG_A_PIXEL

        # Imagen y flip
        imagen = jugador.animations[jugador.frame_index]
        if jugador.flip:
            imagen = pygame.transform.flip(imagen, True, False)

        player_img = pygame.transform.scale(imagen, (int(ancho_pixeles), int(altura_pixeles)))

        # POSICIÓN

         # Y ajustada
        pos_y = -35 + (c.alto // 2)

        # Línea base para pies del personaje base
        pos_pies_y = pos_y  + 150
        
        # X centrado en base a ancho nuevo
        pos_x = c.ancho * 0.1 + 75 -(1/2)*ancho_pixeles 
       
        player_pos = (pos_x, pos_pies_y-int(altura_pixeles))

        enemy_img = pygame.transform.scale(
            pygame.transform.flip(enemigo.animations[enemigo.frame_index], True, False),
            (int(ancho_pixeles_enemigo), int(altura_pixeles_enemigo))
        )

        pos_xe = c.ancho * 0.7 + 75 -(1/2)*ancho_pixeles_enemigo 
        enemy_pos = (pos_xe,pos_pies_y-int(altura_pixeles_enemigo))



        screen.blit(player_img, player_pos)
        screen.blit(enemy_img, enemy_pos)
        
        # Dibujar texto de combate
        text = font.render("COMBATE! Presiona ESC para huir", True, (255, 255, 255))
        screen.blit(text, (c.ancho // 2 - text.get_width() // 2, 50))
        
        # Dibujar opciones de combate
        lugar = 480
        menu_turno_visual(small_font)
            
        # Mostrar estadísticas
        player_stats = small_font.render(f"{jugador.nombre}: HP {jugador.vida}", True, (255, 255, 255))
        enemy_stats = small_font.render(f"{enemigo.nombre}: HP {enemigo.vida}", True, (255, 255, 255))
        screen.blit(player_stats, (c.ancho * 0.1, 100))
        screen.blit(enemy_stats, (c.ancho * 0.7, 100))

        if atac_act:
            menu_atac_visual(small_font)

        if damage_act:
            dibujar_texto(f"{deamage_valu}", 300, lugar, small_font)

        #barras de vida
        pygame.draw.rect(screen, (255,255,255), (c.ancho * 0.1, 120, 160*(jugador.vida/jugador.vida_maxima), 30), 0)
        pygame.draw.rect(screen, (255,255,255), (c.ancho * 0.7, 120, 160*(enemigo.vida/enemigo.vida_maxima), 30), 0)
        pygame.draw.rect(screen, (0,0,255), (c.ancho * 0.1, 120, 160, 30), 2)
        pygame.draw.rect(screen, (255,0,0), (c.ancho * 0.7, 120, 160, 30), 2)

        pygame.display.update()
        clock.tick(c.FPS*0.2)

    elif game_state == "combat_end":#optimisar quitar lienas
        jugador.frame_index = (jugador.frame_index + 1) % len(jugador.animations)
        enemigo.frame_index = (enemigo.frame_index + 1) % len(enemigo.animations)
    
        screen.blit(background, (0, 0))       
       
        altura_pixeles = jugador.altura * c.RELACION_CM_A_PIXEL
        ancho_pixeles = jugador.peso * c.RELACION_KG_A_PIXEL

        altura_pixeles_enemigo = enemigo.altura * c.RELACION_CM_A_PIXEL
        ancho_pixeles_enemigo = enemigo.peso * c.RELACION_KG_A_PIXEL
     
        imagen = jugador.animations[jugador.frame_index]
        if jugador.flip:
            imagen = pygame.transform.flip(imagen, True, False)

        player_img = pygame.transform.scale(imagen, (int(ancho_pixeles), int(altura_pixeles)))
        pos_y = -35 + (c.alto // 2)
        pos_pies_y = pos_y  + 150
        pos_x = c.ancho * 0.1 + 75 -(1/2)*ancho_pixeles  
        player_pos = (pos_x, pos_pies_y-int(altura_pixeles))
        enemy_img = pygame.transform.scale(
            pygame.transform.flip(enemigo.animations[enemigo.frame_index], True, False),
            (int(ancho_pixeles_enemigo), int(altura_pixeles_enemigo))
        )

        pos_xe = c.ancho * 0.7 + 75 -(1/2)*ancho_pixeles_enemigo 
        enemy_pos = (-10000,pos_pies_y-int(altura_pixeles_enemigo))
        screen.blit(player_img, player_pos)
        screen.blit(enemy_img, enemy_pos)

        #IMPORTANTE
        if end:
            dibujar_texto(f"{exp_ga}/{exp_re} xp", 360, lugar, small_font)

        # Instrucciones para continuar
        continuar_text = small_font.render("Presiona E para continuar", True, (255, 255, 255))
        screen.blit(continuar_text, (c.ancho // 2 - continuar_text.get_width() // 2, 300))

        # Manejo de eventos (fuera del bucle for principal)
       

        pygame.display.update()
        clock.tick(c.FPS*0.2)

    elif game_state == "game over":
        screen.fill((0,0,0))

        gameover = small_font.render(f"GAME OVER", True, (255, 255, 255))
        screen.blit(gameover, (c.ancho * 0.5, 100))

    elif game_state == "inventario":
            screen.fill((80,0,0))
            #if op="arma":
             #   dibujar_texto()

    pygame.display.update()
    clock.tick(c.FPS)    

pygame.quit()
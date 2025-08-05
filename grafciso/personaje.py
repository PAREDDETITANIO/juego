import pygame
import constantes as c
import random as r
import weapons as a
import armaduras as ar
def ber(p):
    return r.choices([0, 1], weights=[1-p, p])[0]

def scal_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))

def dibujar_texto(screen,texto, x, y, fuente, color=(255, 255, 255)):
    superficie = fuente.render(texto, True, color)
    screen.blit(superficie, (x, y))
                

class Player():
    def __init__(self,x,y,animations,screen,nombre, vida, fuerza, velocidad, inteligencia, defensa, suerte,fe,mana=100, raza=None):
        
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x,y)
        self.in_combat = False
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida  
        self.fuerza = fuerza
        self.velocidad = velocidad
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.suerte = suerte
        self.fe=fe
        self.mana = mana if mana is not None else 100
        self.lvl = 1
        self.exp=0
        self.vida_base = vida 
        self.defensa_base = defensa
        self.fuerza_base = fuerza
        self.singularidad=[]

        self.screen=screen
        self.equipo = {
        "arma": None,
        "armadura": None
        }
        self.inventario = {
            "armas": [],
            "armaduras": [],
            "pociones": [2,0,0]
                }  
        self.efectos_activos = []
        if raza == None:
            self.preguntar_raza(screen)
        else:
            self.raza = raza
        self.medida()
        self.singularidades()
        self.actualizar_vida_mana_maxima()

# Animacion
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
        #pygame.draw.rect(interfaz, (255,255,255),self.shape,1)
                         

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

# Funciones de juego
    def expc(self, nivel_enemigo):
        exp_ganada = int(75 * (1.15 ** nivel_enemigo))
        self.exp += exp_ganada
        
        exp_requerida_levelup = int(100 * (1.15 ** self.lvl))
        if self.exp >= exp_requerida_levelup:
            self.exp -= exp_requerida_levelup
            self.levelup()
        
        return exp_ganada , exp_requerida_levelup
    
    
    def get_mana(self):
        return self.mana

    def pick(self,item):
        if isinstance(item, a.Arma):
            self.inventario["armas"].append(item)
            print(f"\n¡Has obtenido un arma!")
            print(item)
        elif isinstance(item, ar.Armadura):
            self.inventario["armaduras"].append(item)
            print(f"\n¡Has obtenido un armadura!")
            print(item)
        else:
            print("Tipo de ítem desconocido.")

    def ver_invent(self,item):
        if item==1:
            for i in range(len(self.inventario["armas"])):
                print(f"\nnumero: {i}")
                print(self.inventario["armas"][i].__str__())
        if item==2:
            for i in range(len(self.inventario["armaduras"])):
                print(f"\nnumero: {i}")
                print(self.inventario["armaduras"][i].__str__())
        if item==3:
            print("\ncantidad de posiones:")
            print(f"1-posiones menores: {self.inventario["pociones"][0]}")
            print(f"1-posiones medias: {self.inventario["pociones"][1]}")
            print(f"1-posiones mayores: {self.inventario["pociones"][2]}")

    def eliminar_inv(self):

        item=int(input("\nelije armas(1) armaduras(2): "))
        if item==1:
            for i in range(len(self.inventario["armas"])):
                print(f"\nnumero: {i+1}")
                print(self.inventario["armas"][i].__str__())
            opcion=int(input("\nselecciona un numero para eliminar: "))
            if opcion <= len(self.inventario["armas"]):
                self.inventario["armas"].pop(opcion-1)
                print(f"haz eliminado el arma numero {opcion}")   
            else:
                print("no tienes ese item")   

        if item==2:
            for i in range(len(self.inventario["armaduras"])):
                print(f"\nnumero: {i+1}")
                print(self.inventario["armaduras"][i].__str__())
            opcion=int(input("\nselecciona un numero para eliminar: "))
            if opcion <= len(self.inventario["armaduras"]):
                self.inventario["armaduras"].pop(opcion-1)
                print(f"haz eliminado la armadura numero {opcion}")   
            else:
                print("\nno tienes ese item") 

    def equipar_arma(self):
        self.ver_invent(1)
        indice=int(input("\nElije:"))
        if 0 <= indice < len(self.inventario["armas"]) and self.lvl >=self.inventario["armas"][indice].lvl :
            self.equipo["arma"] = self.inventario["armas"][indice]
            print(f"\nHas equipado el arma: {self.equipo['arma'].name}")
        elif self.lvl < self.inventario["armas"][indice].lvl:
            print("\nLvl bajo")
        else:
            print("\nIndice invalido")    

    def equipar_armadura(self): 
        self.ver_invent(2)
        try:
            indice = int(input("\nElije:"))
            if 0 <= indice < len(self.inventario["armaduras"]):
                # Guardar stats antes del cambio
                vida_actual = self.vida
                porcentaje_vida = vida_actual / self.vida_maxima if self.vida_maxima > 0 else 1
                
                # Remover bonus de armadura actual (si hay una equipada)
                if self.equipo["armadura"]:
                    armadura_actual = self.equipo["armadura"]
                    self.defensa -= armadura_actual.defensa
                    self.vida_maxima -= armadura_actual.vida
                    self.velocidad -= armadura_actual.vel
                
                # Equipar nueva armadura
                nueva_armadura = self.inventario["armaduras"][indice]
                self.equipo["armadura"] = nueva_armadura
                
                # Aplicar bonus de nueva armadura
                self.defensa += nueva_armadura.defensa
                self.vida_maxima += nueva_armadura.vida
                self.velocidad += nueva_armadura.vel
                
                # Ajustar vida actual proporcionalmente
                self.vida = int(self.vida_maxima * porcentaje_vida)
                
                print(f"\nHas equipado: {nueva_armadura.name}")
                print(f"Defensa total: {self.defensa_total()}")
                print(f"Vida máxima: {self.vida_maxima}")
                print(f"Velocidad total: {self.velocidad_total()}")
            else:
                print("Índice inválido")
        except ValueError:
            print("Por favor ingresa un número válido")

    def vida_total(self):
        return self.vida_maxima 

    def fuerza_total(self):
        return self.fuerza + (self.equipo["arma"].damage if self.equipo["arma"] else 0)

    def inteligencia_total(self):
        return self.inteligencia + (self.equipo["arma"].damage if self.equipo["arma"] else 0)

    def fe_total(self):
        return self.fe + (self.equipo["arma"].damage if self.equipo["arma"] else 0)
        
    def defensa_total(self):
        return self.defensa  

    def velocidad_total(self):
        return self.velocidad  

    def actualizar_vida_mana_maxima(self):
        self.vida_maxima = self.vida
        self.mana_maxima = self.mana  
    @property
    def recurso_nombre(self):
        if isinstance(self, Mago):
            return "Mana"
        elif isinstance(self, Guerrero):
            return "Stamina"
        elif isinstance(self, Templario):
            return "Rezo"
        elif isinstance(self, Cientifico):
            return "Energia"
        elif isinstance(self, Samurai):
            return "Stamina"
        else:
            return "Oscuridad"

    def mostrar_atributos(self, superficie):
        """Dibuja los atributos en una superficie dada"""
        # Configuración visual
        margen = 20
        interlineado = 25
        x = margen
        y = margen
        
        # Crear fondo semitransparente
        background = pygame.Surface((300, 400), pygame.SRCALPHA)
        background.fill((64, 64, 64))  # gris semitransparente
        superficie.blit(background, (x, y))
        
        # Fuentes
        titulo_font = pygame.font.SysFont('Arial', 24, bold=True)
        texto_font = pygame.font.SysFont('Arial', 18)
        
        # Dibujar título
        self._dibujar_texto(superficie, f"{self.nombre} - Nivel {self.lvl}", 
                        x + margen, y + margen, titulo_font, (255, 215, 0))
        y += interlineado * 1.5
        
        # Primera columna (stats principales)
        stats_principales = [
            f"Raza: {self.raza}",
            f"Vida: {self.vida}/{self.vida_maxima}",
            f"{self.recurso_nombre}: {self.mana}/{self.mana_maxima}",
            f"Defensa: {self.defensa}",
            f"Suerte: {self.suerte}",
            f"Velocidad: {self.velocidad}",
            f"singularidades: {self.singularidad}"
            
            
        ]
        
        for stat in stats_principales:
            self._dibujar_texto(superficie, stat, x + margen, y + margen, texto_font)
            y += interlineado
        
        # Segunda columna (stats secundarios)
        y = margen + interlineado * 1.5  # Reset Y position
        x += 150  # Mover a la derecha para segunda columna
        
        stats_secundarios = [
            f"Fuerza: {self.fuerza}",
            f"Fe: {self.fe}",
            f"Inteligencia: {self.inteligencia} iq",
            
            f"Altura: {self.altura}cm",
            f"Peso: {self.peso}kg",
            
           
        ]
        
        for stat in stats_secundarios:
            self._dibujar_texto(superficie, stat, x + margen, y + margen, texto_font)
            y += interlineado

    def _dibujar_texto(self, superficie, texto, x, y, fuente, color=(255, 255, 255)):
        """Método helper para dibujar texto con sombra"""
        # Sombra
        sombra = fuente.render(texto, True, (0, 0, 0))
        superficie.blit(sombra, (x + 1, y + 1))
        # Texto principal
        texto_surface = fuente.render(texto, True, color)
        superficie.blit(texto_surface, (x, y))

    def preguntar_raza(self, screen):
        razas = [
            ("Humano", "+fe"),
            ("Elfo", "+inteligencia, +fe"),
            ("Demonio", "+fuerza, +vel, -fe, -suerte"),
            ("Orco", "+fuerza, -inteligencia"),
            ("Dracónido", "NO SE TODAVIA: +suerte")
        ]
        
        # Configuración visual
        background = pygame.Surface((c.ancho, c.alto), pygame.SRCALPHA)
        background.fill((0, 0, 0, 200))  # Fondo semitransparente
        
        title_font = pygame.font.SysFont(None, 48)
        option_font = pygame.font.SysFont(None, 36)
        desc_font = pygame.font.SysFont(None, 24)
        
        selected = 0
        choosing = True
        
        while choosing:
            # Dibujar fondo semitransparente
            screen.blit(background, (0, 0))
            
            # Título
            title = title_font.render("SELECCIONA TU RAZA", True, (255, 255, 255))
            screen.blit(title, (c.ancho//2 - title.get_width()//2, 50))
            
            # Opciones de raza
            for i, (raza, desc) in enumerate(razas):
                y_pos = 150 + i * 80
                color = (255, 215, 0) if i == selected else (255, 255, 255)
                
                # Número y nombre de raza
                raza_text = option_font.render(f"{i+1}. {raza}", True, color)
                screen.blit(raza_text, (c.ancho//2 - 200, y_pos))
                
                # Descripción del bono
                desc_text = desc_font.render(desc, True, (200, 200, 200))
                screen.blit(desc_text, (c.ancho//2 - 200, y_pos + 30))
            
            # Instrucciones
            instrucciones = desc_font.render("↑ ↓ para navegar | ENTER para seleccionar", True, (200, 200, 200))
            screen.blit(instrucciones, (c.ancho//2 - instrucciones.get_width()//2, c.alto - 50))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(razas)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(razas)
                    elif event.key == pygame.K_RETURN:
                        self.raza = razas[selected][0]

                        self.aplicar_bono_racial()
                        self.actualizar_vida_mana_maxima()
                        

                        # Mostrar confirmación
                        confirmacion = title_font.render(f"Raza seleccionada: {self.raza}", True, (0, 255, 0))
                        screen.blit(confirmacion, (c.ancho//2 - confirmacion.get_width()//2, c.alto//2))
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        
                        choosing = False
                    elif event.key == pygame.K_ESCAPE:
                        choosing = False

    def aplicar_bono_racial(self):

        if self.raza == "Humano" :
            self.vida += 10  
            self.fuerza += 5 
            self.velocidad += 2 
            self.inteligencia += 5 
            self.defensa += 2
            self.suerte += 5
            self.fe += 15
            self.mana += 10

        elif self.raza == "Elfo":
            self.vida += 12  
            self.fuerza += 5 
            self.velocidad += 10 
            self.inteligencia += 15 
            self.defensa += 0
            self.suerte += 2
            self.fe += 10
            self.mana += 12
        elif self.raza == "Orco":
            self.vida += 20  
            self.fuerza += 15 
            self.velocidad += 0 
            self.inteligencia -= 5 
            self.defensa += 10
            self.suerte += 0
            self.fe += 0
            self.mana += 8
        elif self.raza == "Demonio":  
            self.vida += 16  
            self.fuerza += 12 
            self.velocidad += 10 
            self.inteligencia += 8
            self.defensa += 5
            self.suerte -= 2
            self.fe += -10  
            self.mana += 20
        elif self.raza == "Dracónido":
            self.vida += 18
            self.fuerza += 12
            self.velocidad += 4
            self.inteligencia += 8
            self.defensa += 6
            self.suerte += 1
            self.fe += 5
            self.mana += 15    

    def levelup(self):
        if self.lvl<50:
            self.lvl += 1
            self.vida += 5
            self.mana += 5
            self.fuerza += 1
            self.velocidad += 1
            self.inteligencia += 1
            self.defensa += 1
            self.suerte += 1
            self.vida_maxima += 5
            self.mana_maxima += 5
        else:
            self.lvl += 1
            self.vida += 10
            self.mana += 10
            self.fuerza += 2
            self.velocidad += 2
            self.inteligencia += 2
            self.defensa += 2
            self.suerte += 2
            self.vida_maxima += 10   
            self.mana_maxima += 10 
        print(f"{self.nombre} subió de nivel")

    def vivo(self):
        return self.vida > 0
    
    def matar(self):
        self.vida = 0
        print(f"{self.nombre} ha muerto")

    def damage(self,enemigo):
        return self.fuerza-enemigo.defensa   

    def ataque(self, enemigo):
        damage = self.damage(enemigo)
        enemigo.vida -= damage

    
        if enemigo.vivo():
            print("\ndamage de", self.nombre, ":", damage)
            print("vida de", enemigo.nombre, ":", enemigo.vida, "/", enemigo.vida_maxima)
        else:
            print("\ndamage de", self.nombre, ":", damage)
            print("vida de", enemigo.nombre, 0)
            enemigo.matar()

    def curar(self, tipo):
        if self.inventario["pociones"][tipo-1] > 0:
            if tipo == 0:
                curacion = int(self.vida_maxima * 0.2)
            elif tipo == 1:
                curacion = int(self.vida_maxima * 0.5)
            elif tipo == 2:
                curacion = int(self.vida_maxima * 0.8)
            else:
                print("Tipo de poción inválido.")
                return

            vida_faltante = self.vida_maxima - self.vida
            ganancia = min(curacion, vida_faltante)
            self.vida += ganancia
            self.inventario["pociones"][tipo-1] -= 1
            print(f"Te curaste {ganancia} HP. (Vida: {self.vida}/{self.vida_maxima})")
        else:
            print("No te queda de esa poción.")

    def medida(self):
        if self.raza == "Humano":
            self.altura = int(r.gauss(170,7)) 
            imc = int(r.gauss(24, 4))     
            self.peso = int(imc*((self.altura/100)**2))
        elif self.raza == "Elfo":
            self.altura = int(r.gauss(185,7)) 
            imc = int(r.gauss(22, 4))     
            self.peso = int(imc*((self.altura/100)**2))
        elif self.raza == "Orco":
            self.altura = int(r.gauss(200,7)) 
            imc = int(r.gauss(31, 4))     
            self.peso = int(imc*((self.altura/100)**2))
        elif self.raza == "Demonio":  
            self.altura = int(r.gauss(185,7)) 
            imc = int(r.gauss(24, 4))     
            self.peso = int(imc*((self.altura/100)**2))
        elif self.raza == "Dracónido":
            self.altura = int(r.gauss(195,7)) 
            imc = int(r.gauss(26, 4))     
            self.peso = int(imc*((self.altura/100)**2))

    def singularidades(self):
        prob={
            "down": 1/100,
            "superdotacion": 1/50,
            "gigantismo": 1/75,
            "cancer":1/60,
            "enano": 1/50
            }

        if ber(prob["superdotacion"])==1: 
            self.inteligencia = int(max(130, r.gauss(135.5,5.4)))   
            self.singularidad.append("superdotacion")
        if ber(prob["down"])==1:
            self.fuerza -= 10
            self.inteligencia -= 30
            self.altura -= 10
            self.peso += 5
            self.singularidad.append("down")
        if ber(prob["gigantismo"])==1:
            self.fuerza += 10
            self.inteligencia -= 5
            self.altura += 30
            self.peso += 50
            self.singularidad.append("gigantismo")
        if ber(prob["cancer"])==1:
            self.fe +=30
            #si pasan 15 turnos moris
            self.singularidad.append("cancer")
        if ber(prob["enano"]):
            self.altura -= 30
            self.singularidad.append("enano")



        

        


class Enemy(Player):
    def __init__(self, x, y, animations,screen,nombre="fabio", vida=None, fuerza=None, velocidad=None, inteligencia=None, defensa=None, suerte=None,fe=None,mana=None, raza=None):
        super().__init__(x, y, animations,screen, nombre,
            mana=int(r.gauss(90, 10)) if mana is None else mana,
            vida=int(r.gauss(90, 10)) if vida is None else vida,
            fe=int(r.gauss(8, 1)) if fe is None else fe,
            fuerza=int(r.gauss(8, 1)) if fuerza is None else fuerza,
            velocidad=int(r.gauss(8, 1)) if velocidad is None else velocidad,
            inteligencia=int(r.gauss(80, 10)) if inteligencia is None else inteligencia,
            defensa=int(r.gauss(8, 1)) if defensa is None else defensa,
            suerte=int(r.gauss(1, 0.2)) if suerte is None else suerte,
            raza=raza)
        self.speed = 1
        self.detection_radius = 500
        self.dx = 0
        self.dy = 0
        self.state = "idle"
        self.preguntar_raza(screen)
          
    def mostrar_atributos(self, superficie):
        """Dibuja los atributos en una superficie dada"""
        # Configuración visual
        margen = 20
        interlineado = 25
        x = margen
        y = margen
        
        # Crear fondo semitransparente
        background = pygame.Surface((300, 400), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Negro semitransparente
        superficie.blit(background, (x, y))
        
        # Fuentes
        titulo_font = pygame.font.SysFont('Arial', 24, bold=True)
        texto_font = pygame.font.SysFont('Arial', 18)
        
        # Dibujar título
        self._dibujar_texto(superficie, f"{self.nombre} - Nivel {self.lvl}", 
                        x + margen+400, y + margen, titulo_font, (255, 215, 0))
        y += interlineado * 1.5
        
        # Primera columna (stats principales)
        stats_principales = [
            f"Raza: {self.raza}",
            f"Vida: {self.vida}/{self.vida_maxima}",
            f"{self.recurso_nombre}: {self.mana}/{self.mana_maxima}",
            f"Defensa: {self.defensa}",
            f"Suerte: {self.suerte}",
            f"Velocidad: {self.velocidad}",
            f"singularidades: {self.singularidad}"
            
            
        ]
        
        for stat in stats_principales:
            self._dibujar_texto(superficie, stat, x + margen+400, y + margen, texto_font)
            y += interlineado
        
        # Segunda columna (stats secundarios)
        y = margen + interlineado * 1.5  # Reset Y position
        x += 150  # Mover a la derecha para segunda columna
        
        stats_secundarios = [
            f"Fuerza: {self.fuerza}",
            f"Fe: {self.fe}",
            f"Inteligencia: {self.inteligencia} iq",
            
            f"Altura: {self.altura}cm",
            f"Peso: {self.peso}kg",
            
           
        ]
        
        for stat in stats_secundarios:
            self._dibujar_texto(superficie, stat, x + margen+400, y + margen, texto_font)
            y += interlineado



        
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
    
    def preguntar_raza(self,screen):      
        while True:
            eleccion = r.choice([1,2,3,4,5])
            if eleccion == 1:
                self.raza = "Humano"
                break
            elif eleccion == 2:
                self.raza = "Elfo"
                break
            elif eleccion == 3:
                self.raza = "Demonio"
                break
            elif eleccion == 4:
                self.raza = "Orco"
                break
            elif eleccion == 5:
                self.raza = "Dracónido"
                break
            else:
                pass
        self.aplicar_bono_racial()
        self.actualizar_vida_mana_maxima()

    def aplicar_bono_racial(self):
        if self.raza == "Humano":
            self.vida += 10  
            self.fuerza += 5 
            self.velocidad += 2 
            self.inteligencia += 5 
            self.defensa += 2
            self.suerte += 5
            self.fe += 15
            self.mana += 10
        elif self.raza == "Elfo":
            self.vida += 12  
            self.fuerza += 5 
            self.velocidad += 10 
            self.inteligencia += 15 
            self.defensa += 0
            self.suerte += 2
            self.fe += 10
            self.mana += 12
        elif self.raza == "Orco":
            self.vida += 20  
            self.fuerza += 15 
            self.velocidad += 0 
            self.inteligencia -= 5 
            self.defensa += 10
            self.suerte += 0
            self.fe += 0
            self.mana += 8
        elif self.raza == "Demonio":  
            self.vida += 16  
            self.fuerza += 8 
            self.velocidad += 5 
            self.inteligencia += 10 
            self.defensa += 5
            self.suerte += 4
            self.fe += -10  
            self.mana += 20
        elif self.raza == "Dracónido":
            self.vida += 18
            self.fuerza += 12
            self.velocidad += 4
            self.inteligencia += 8
            self.defensa += 6
            self.suerte += 1
            self.fe += 5
            self.mana += 15      
  
    def levelup(self):
        if self.lvl<50:
            self.lvl += 1
            self.vida += 5
            self.mana += 5
            self.fuerza += 1
            self.velocidad += 1
            self.inteligencia += 1
            self.defensa += 1
            self.suerte += 1
            self.vida_maxima += 5
        else:
            self.lvl += 1
            self.vida += 10
            self.mana += 10
            self.fuerza += 2
            self.velocidad += 2
            self.inteligencia += 2
            self.defensa += 2
            self.suerte += 2
            self.vida_maxima += 10

    def damage(self, enemigo):
        poder_inteligencia = self.inteligencia - 90
        poder_fuerza = self.fuerza
        poder_fe = self.fe

        mejor_poder = max(poder_fuerza, poder_inteligencia, poder_fe)
        
        if mejor_poder < enemigo.defensa:
            return 0
        else:
            if ber(self.suerte * 0.01) == 0:  
                return max(1, mejor_poder - enemigo.defensa) 
            else:  # Crítico
                return max(1, 2 * mejor_poder - enemigo.defensa)









class Guerrero(Player):
    def __init__(self, x, y, animations,screen,nombre, vida=110, fuerza=15, velocidad=10, inteligencia=90, defensa=15, suerte=1, fe=10 ,mana=100, raza=None):
        super().__init__(x, y, animations,screen,nombre, vida, fuerza, velocidad, inteligencia, defensa, suerte, fe, mana, raza)

        animations_w = []
        for i in range(10):
            image_sword = pygame.image.load(f"C:/Users/giost/OneDrive/Escritorio/pygame/grafciso/assets/imagen/weapons/sprite_{i}.png")
            animations_w.append(scal_img(image_sword, c.scala_w))

        arma_inicial = a.Arma_g(animations_w,lvl_P=1, suerte=self.suerte, damage=5, lvl=0, vel=0, rareza="normal")
        self.inventario["armas"].append(arma_inicial)
        self.equipo["arma"] = arma_inicial


    def damage(self,enemigo):
        arma = self.equipo["arma"]
        arma_damage = arma.damage if arma else 0 
            
        poder = self.fuerza_total()
        if poder < enemigo.defensa:
            return 0
        if ber(self.suerte * 0.01) == 0:
            return poder - enemigo.defensa
        else:
            return 2 * poder - enemigo.defensa
                  
class Mago(Player):
    def __init__(self, x, y, animations,screen, nombre, vida=100, fuerza=8, velocidad=11, 
                 inteligencia=110, defensa=8, suerte=1,fe=15,mana=140, raza=None):   
        super().__init__( x, y, animations,screen,nombre, vida, fuerza, velocidad, inteligencia,
                         defensa, suerte, fe, mana, raza)

        animations_w = []
        for i in range(10):
            image_sword = pygame.image.load(f"grafciso/assets/imagen/weapons/sprite_{i}.png")
            animations_w.append(scal_img(image_sword, c.scala_w))

        arma_inicial = a.Arma_m(animations_w,lvl_P=1, suerte=self.suerte, damage=5, lvl=0, vel=0, rareza="normal")
        self.inventario["armas"].append(arma_inicial)
        self.equipo["arma"] = arma_inicial

    def damage(self,enemigo):
        arma = self.equipo["arma"]
        arma_damage = arma.damage if arma else 0 
            
        poder = int((self.inteligencia-90+ self.fe)/1.8) + arma_damage
        if poder < enemigo.defensa:
            return 0
        if ber(self.suerte * 0.01) == 0:
            return poder - enemigo.defensa
        else:
            return 2 * poder - enemigo.defensa




class Templario(Player):
    def __init__(self, x, y, animations,screen, nombre, vida=100, fuerza=12, velocidad=12, 
                 inteligencia=100, defensa=12, suerte=5,fe=20,mana=130, raza=None):   
        super().__init__(x, y, animations,screen,nombre, vida, fuerza, velocidad, inteligencia,
                         defensa, suerte, fe, mana, raza)

        animations_w = []
        for i in range(10):
            image_sword = pygame.image.load(f"grafciso/assets/imagen/weapons/sprite_{i}.png")
            animations_w.append(scal_img(image_sword, c.scala_w))

        
        arma_inicial = a.Arma_t(animations_w=animations_w,lvl_P=1, suerte=self.suerte, damage=5, lvl=0, vel=0, rareza="normal")
        self.inventario["armas"].append(arma_inicial)
        self.equipo["arma"] = arma_inicial

    def damage(self,enemigo):
        arma = self.equipo["arma"]
        arma_damage = arma.damage if arma else 0 
            
        poder = self.fe_total()
        if poder < enemigo.defensa:
            return 0
        if ber(self.suerte * 0.01) == 0:
            return poder - enemigo.defensa
        else:
            return 2 * poder - enemigo.defensa
        

    def aplicar_bono_racial(self):
        if self.raza == "Humano" :
            self.vida += 10  
            self.fuerza += 5 
            self.velocidad += 2 
            self.inteligencia += 5 
            self.defensa += 2
            self.suerte += 5
            self.fe += 15
            self.mana += 10
        elif self.raza == "Elfo":
            self.vida += 12  
            self.fuerza += 5 
            self.velocidad += 10 
            self.inteligencia += 15 
            self.defensa += 0
            self.suerte += 2
            self.fe += 10
            self.mana += 12
        elif self.raza == "Orco":
            self.vida += 20  
            self.fuerza += 15 
            self.velocidad += 0 
            self.inteligencia -= 5 
            self.defensa += 10
            self.suerte += 0
            self.fe += 0
            self.mana += 8
        elif self.raza == "Demonio" and self.nombre=="LUCIFER":  
            self.vida += 25  
            self.fuerza += 20 
            self.velocidad += 20 
            self.inteligencia += 20 
            self.defensa += 15
            self.suerte += 0
            self.fe += 50  
            self.mana += 25
        elif self.raza == "Dracónido":
            self.vida += 18
            self.fuerza += 12
            self.velocidad += 4
            self.inteligencia += 8
            self.defensa += 6
            self.suerte += 1
            self.fe += 5
            self.mana += 15    
         
class Cientifico(Player):
    def __init__(self, x, y, animations, screen, nombre, vida=100, fuerza=8, velocidad=10, inteligencia=120,
                 defensa=10, suerte=10, fe=0, mana=120, raza=None):
        super().__init__(x, y, animations ,screen ,nombre, vida, fuerza, velocidad, inteligencia,
                         defensa, suerte, fe, mana, raza)
        animations_w = []
        for i in range(10):
            image_sword = pygame.image.load(f"grafciso/assets/imagen/weapons/sprite_{i}.png")
            animations_w.append(scal_img(image_sword, c.scala_w))

        
        arma_inicial = a.Arma_c(animations_w=animations_w,lvl_P=1, suerte=self.suerte, damage=5, lvl=0, vel=0, rareza="normal")
        self.inventario["armas"].append(arma_inicial)
        self.equipo["arma"] = arma_inicial


    def damage(self, enemigo):
        arma = self.equipo["arma"]
        arma_damage = arma.damage if arma else 0
        
        poder = self.inteligencia_total()-90
        if poder < enemigo.defensa:
            return 0
        if ber(self.suerte * 0.01) == 0:
            return poder - enemigo.defensa
        else:
            return 2 * poder - enemigo.defensa
     

    def aplicar_bono_racial(self):
        if self.raza == "Humano" and self.nombre == "a":
            self.vida += 10  
            self.fuerza += 5 
            self.velocidad += 20 
            self.inteligencia += 40 
            self.defensa += 20
            self.suerte += 20
            self.fe -= 20
            self.mana += 30
        elif self.raza == "Elfo":
            self.vida += 12  
            self.fuerza += 5 
            self.velocidad += 10 
            self.inteligencia += 15 
            self.defensa += 0
            self.suerte += 2
            self.fe += 10
            self.mana += 12
        elif self.raza == "Orco":
            self.vida += 20  
            self.fuerza += 15 
            self.velocidad += 0 
            self.inteligencia -= 5 
            self.defensa += 10
            self.suerte += 0
            self.fe += 0
            self.mana += 8
        elif self.raza == "Demonio":  
            self.vida += 16  
            self.fuerza += 8 
            self.velocidad += 5 
            self.inteligencia += 10 
            self.defensa += 5
            self.suerte += 4
            self.fe += -10  
            self.mana += 20
        elif self.raza == "Dracónido":
            self.vida += 18
            self.fuerza += 12
            self.velocidad += 4
            self.inteligencia += 8
            self.defensa += 6
            self.suerte += 1
            self.fe += 5
            self.mana += 15                 
#def __init__(self,x,y,animations,screen,nombre, vida, fuerza, velocidad, inteligencia, defensa, suerte,fe,mana=100, raza=None):
class Samurai(Player):
    def __init__(self, x, y, animations,screen, nombre, vida=100, fuerza=15, velocidad=15, inteligencia=110,
                 defensa=10, suerte=5, fe=10, mana=110, raza=None):
        super().__init__(x, y, animations,screen, nombre, vida, fuerza, velocidad, inteligencia,
                         defensa, suerte, fe, mana, raza)
        animations_w = []
        for i in range(10):
            image_sword = pygame.image.load(f"grafciso/assets/imagen/weapons/sprite_{i}.png")
            animations_w.append(scal_img(image_sword, c.scala_w))

        arma_inicial = a.Arma_s(animations_w,lvl_P=1, suerte=self.suerte, damage=5, lvl=0, vel=0, rareza="normal")
        self.inventario["armas"].append(arma_inicial)
        self.equipo["arma"] = arma_inicial


    def damage(self, enemigo):
        arma = self.equipo["arma"]
        arma_damage = arma.damage if arma else 0
        
        poder =int( (self.fuerza_total() + self.velocidad_total())/1.8)
        if poder < enemigo.defensa:
            return 0
        if ber(self.suerte * 0.01) == 0:
            return poder - enemigo.defensa
        else:
            return 2 * poder - enemigo.defensa



import pygame
import constantes as c
import random as r


class Weapons():
    
    def __init__(self,animations_w,lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):

        self.frame_index=0
        self.animations_w = animations_w
        self.image = animations_w[self.frame_index]
        self.shape = self.image.get_rect()
        self.update_time = pygame.time.get_ticks()
        self.lvl_p = lvl_P
        self.suerte = suerte
        self.damage = damage
        self.vel = vel
        self.lvl = lvl
        self.rareza = rareza
        self.efectos_activos = []
        
# Graficos
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

# logica
    def seleccionar_nombre(self, armas, pesos):
        self.name = r.choices(armas, weights=pesos, k=1)[0]

    def calcular_stats_base(self, base_damage, base_vel, escala_nivel):
        self.damage = int(r.gauss(base_damage, base_damage * 0.2)) if self.damage is None else self.damage
        self.vel = int(r.gauss(base_vel, base_vel * 0.2)) if self.vel is None else self.vel
        self.lvl = int(((self.damage / base_damage + self.vel / base_vel) / 2) * escala_nivel)

    def determinar_rareza(self, escala_nivel):
        valores_rareza = {
            "normal": 0,
            "raro": 1,
            "épico": 2,
            "legendario": 3,
            "mítico": 4,
            "divino": 5
        }

        if self.lvl >= escala_nivel:
            self.rareza = r.choice(["épico", "legendario", "mítico", "divino"])
        else:
            self.rareza = r.choice(["normal", "raro"])

        escalado = valores_rareza[self.rareza]

        if escalado != 0:
            self.damage += int(self.damage * escalado * 0.01)
            self.vel += int(self.vel * escalado * 0.01)

        return escalado

    def aplicar_efectos_especiales(self):
        if self.rareza in ["épico", "legendario", "mítico", "divino"]:
            # Definimos valores de escalado según rareza
            escalado = {"épico": 2, "legendario": 3, "mítico": 4, "divino": 5}[self.rareza]
            
            # Efectos disponibles para armas con sus pesos
            efectos_armas = {
                "fuego": 80/3 - self.suerte * 0.1,
                "rayo": 80/3 - self.suerte * 0.1,
                "hielo": 80/3 - self.suerte * 0.1,
                "oscuridad": 20/3 + self.suerte * 0.1,
                "abismo": 20/3 + self.suerte * 0.1,
                "luz": 20/3 + self.suerte * 0.1
            }
            
            # Convertimos a listas separadas para usar con choices
            efectos_disponibles = list(efectos_armas.keys())
            weights = list(efectos_armas.values())
            
            
            num_efectos = min(escalado - 1, len(efectos_disponibles))
            for _ in range(num_efectos):
                if not efectos_disponibles:
                    break
                    
                elegido = r.choices(efectos_disponibles, weights=weights, k=1)[0]
                self.efectos_activos.append(elegido)

                index = efectos_disponibles.index(elegido)
                efectos_disponibles.pop(index)
                weights.pop(index)

    def verificar_combinaciones_especiales(self):
        efectos_elementales = {"fuego", "rayo", "hielo"}
        efectos_ocultos = {"luz", "oscuridad", "abismo"}
        nombres_efectos = set(efecto.lower() for efecto in self.efectos_activos)

        if efectos_elementales.issubset(nombres_efectos):
            self.damage = int(self.damage * 1.5)
            self.vel = int(self.vel * 1.5)
            self.name = f"{self.name.upper()} ELEMENTAL"
        elif efectos_ocultos.issubset(nombres_efectos):
            self.damage = int(self.damage * 1.6)
            self.vel = int(self.vel * 1.6)
            self.name = f"{self.name.upper()} DEL VACÍO"


    
    def __str__(self):
        efectos_str = ', '.join([ef for ef in self.efectos_activos]) if self.efectos_activos else 'Ninguno'
        return (f"{self.name}:\n"
                f"  Daño: {self.damage}\n"
                f"  Velocidad: {self.vel}\n"
                f"  Nivel: {self.lvl}\n"
                f"  Rareza: {self.rareza}\n"
                f"  Efectos especiales: {efectos_str}")



class Arma_g(Weapons):
    def __init__(self,animations_w, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(animations_w,lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Hacha de guerra", "Espada Bastarda", "Mata Dragones"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Hacha de guerra":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Espada Bastarda":
            base_damage = 30 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Mata Dragones":
            base_damage = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) * 1

        self.calcular_stats_base(base_damage, base_vel, escala_nivel)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales()
        self.verificar_combinaciones_especiales()

class Arma_m(Weapons):
    def __init__(self,animations_w, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(animations_w,lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Morellonomicón", "La Biblia Arcana", "Codex Gigas"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Morellonomicón":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "La Biblia Arcana":
            base_damage = 30 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Codex Gigas":
            base_damage = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 12 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) * 1

        self.calcular_stats_base(base_damage, base_vel, escala_nivel)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales()
        self.verificar_combinaciones_especiales()  

class Arma_t(Weapons):
    def __init__(self,animations_w, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(animations_w,lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Baculo De Madera", "Baculo Bendecido", "La Inquisidora"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Baculo De Madera":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Baculo Bendecido":
            base_damage = 30 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "La Inquisidora":
            base_damage = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) * 1

        self.calcular_stats_base(base_damage, base_vel, escala_nivel)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales()
        self.verificar_combinaciones_especiales()

class Arma_c(Weapons):
    def __init__(self,animations_w, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(animations_w,lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Rayo Laser", "Bobina Tesla", "Colisionador De Adrones"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Rayo Laser":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Bobina Tesla":
            base_damage = 30 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Colisionador De Adrones":
            base_damage = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) * 1

        self.calcular_stats_base(base_damage, base_vel, escala_nivel)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales()
        self.verificar_combinaciones_especiales()        

class Arma_s(Weapons):
    def __init__(self, animations_w,lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(animations_w,lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Katana del Viento", "Espada del Amanecer", "Hoja del Dragón"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        if self.name == "Katana del Viento":
            base_damage = 20 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 15 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Espada del Amanecer":
            base_damage = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 20 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 25 + int((self.lvl_p * 0.1)) * 1
        elif self.name == "Hoja del Dragón":
            base_damage = 40 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) * 1

        self.calcular_stats_base(base_damage, base_vel, escala_nivel)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales()
        self.verificar_combinaciones_especiales()  


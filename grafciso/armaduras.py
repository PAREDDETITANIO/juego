import random as r

class Armadura:
    def __init__(self, lvl_P, suerte, vida=None , defensa=None, damage=None, lvl=None, vel=None, rareza=None):
        self.lvl_p = lvl_P
        self.suerte = suerte
        self.damage = damage
        self.defensa=defensa
        self.vida=vida
        self.vel = vel
        self.lvl = lvl
        self.rareza = rareza
        self.efectos_activos = []

    def seleccionar_nombre(self, armadura, pesos):
        self.name = r.choices(armadura, weights=pesos, k=1)[0]

    def calcular_stats_base(self, base_damage, base_vel, escala_nivel,base_vida,base_def):
        self.damage = int(r.gauss(base_damage, base_damage * 0.1)) if self.damage is None else self.damage
        self.vel = int(r.gauss(base_vel, base_vel * 0.2)) if self.vel is None else self.vel
        self.vida=int(r.gauss(base_vida, base_vida * 0.2)) if self.vida is None else self.vida
        self.defensa=int(r.gauss(base_def, base_def * 0.2)) if self.defensa is None else self.defensa
        self.lvl = int(((self.damage / base_damage +self.defensa/base_def +self.vida/base_vida+self.vel / base_vel) / 4) * escala_nivel)

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
            self.vida += int(self.vida * escalado * 0.01)
            self.defensa += int(self.defensa * escalado * 0.01)

        return escalado

    def aplicar_efectos_especiales(self, efectos, escalado):
        if escalado >= 2:
            num_efectos = escalado - 1
            efectos_disponibles = efectos.copy()  
            
            for _ in range(num_efectos):
                if not efectos_disponibles:  
                    break
                elegido = r.choice(efectos_disponibles)
                self.efectos_activos.append(elegido)
                efectos_disponibles.remove(elegido)  

    def verificar_combinaciones_especiales(self):
        efectos_elementales = {"fuego", "rayo", "hielo"}
        efectos_ocultos = {"luz", "oscuridad", "abismo"}
        efectos_actuales = set(self.efectos_activos)

        if efectos_elementales.issubset(efectos_actuales):
            self.damage = int(self.damage * 1.5)
            self.vel = int(self.vel * 1.5)
            self.vida = int(self.vida * 1.5)
            self.defensa = int(self.defensa * 1.5)
            self.name = f"{self.name.upper()} ELEMENTAL"
        elif efectos_ocultos.issubset(efectos_actuales):
            self.damage = int(self.damage * 1.6)
            self.vel = int(self.vel * 1.6)
            self.vida = int(self.vida * 1.6)
            self.defensa = int(self.defensa * 1.6)
            self.name = f"{self.name.upper()} DEL VACÍO"

    def __str__(self):
        return (f"{self.name}:\n"
                f"  Daño: {self.damage}\n"
                f"  Velocidad: {self.vel}\n"
                f"  Vida: {self.vida}\n"
                f"  Defensa: {self.defensa}\n"
                f"  Nivel: {self.lvl}\n"
                f"  Rareza: {self.rareza}\n"
                f"  Efectos especiales: {', '.join(self.efectos_activos) if self.efectos_activos else 'Ninguno'}")

class Armadura_g(Armadura):
    def __init__(self, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Cota de maya", "Armadura Articulada", "Titanio de los Dioses Olvidados"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Cota de maya":
            base_damage = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) 

        elif self.name == "Armadura Articulada":
            base_damage = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) 

        elif self.name == "Titanio de los Dioses Olvidados":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 100 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) 

        self.calcular_stats_base(base_damage, base_vel, escala_nivel,base_vida,base_def)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales(efectos, escalado)
        self.verificar_combinaciones_especiales()

class Armadura_m(Armadura):
    def __init__(self, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Túnica del Sabio Eterno", "Manto del Vacío Abisal", "Armadura del Primigenio"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Túnica del Sabio Eterno":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 12 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 12 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) 
        elif self.name == "Manto del Vacío Abisal":
            base_damage = 20 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 18 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) 
        elif self.name == "Armadura del Primigenio":
            base_damage = 45 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 30 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 20 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) 

        self.calcular_stats_base(base_damage, base_vel, escala_nivel,base_vida,base_def)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales(efectos, escalado)
        self.verificar_combinaciones_especiales()        

class Armadura_t(Armadura):
    def __init__(self, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Cota de maya", "Armadura Articulada", "Titanio de los Dioses Olvidados"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Cota de maya":
            base_damage = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) 

        elif self.name == "Armadura Articulada":
            base_damage = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) 

        elif self.name == "Titanio de los Dioses Olvidados":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 100 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) 

        self.calcular_stats_base(base_damage, base_vel, escala_nivel,base_vida,base_def)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales(efectos, escalado)
        self.verificar_combinaciones_especiales()

class Armadura_c(Armadura):
    def __init__(self, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Cota de maya", "Armadura Articulada", "Titanio de los Dioses Olvidados"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Cota de maya":
            base_damage = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) 

        elif self.name == "Armadura Articulada":
            base_damage = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) 

        elif self.name == "Titanio de los Dioses Olvidados":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 100 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) 

        self.calcular_stats_base(base_damage, base_vel, escala_nivel,base_vida,base_def)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales(efectos, escalado)
        self.verificar_combinaciones_especiales()        

class Armadura_s(Armadura):
    def __init__(self, lvl_P, suerte, damage=None, lvl=None, vel=None, rareza=None):
        super().__init__(lvl_P, suerte, damage, lvl, vel, rareza)
        
        armas = ["Cota de maya", "Armadura Articulada", "Titanio de los Dioses Olvidados"]
        pesos = [60 - self.suerte * 0.1, 30 + self.suerte * 0.05, 10 + self.suerte * 0.05]
        self.seleccionar_nombre(armas, pesos)

        efectos = ['fuego', 'rayo', 'hielo', 'luz', 'oscuridad', 'abismo']
        
        
        if self.name == "Cota de maya":
            base_damage = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 5 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 10 + int((self.lvl_p * 0.1)) 

        elif self.name == "Armadura Articulada":
            base_damage = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 10 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 25 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 20 + int((self.lvl_p * 0.1)) 

        elif self.name == "Titanio de los Dioses Olvidados":
            base_damage = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vel = 15 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_def = 50 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            base_vida = 100 + int((self.lvl_p * 0.1)) * 2 + int((self.suerte * 0.1))
            escala_nivel = 35 + int((self.lvl_p * 0.1)) 

        self.calcular_stats_base(base_damage, base_vel, escala_nivel,base_vida,base_def)
        escalado = self.determinar_rareza(escala_nivel)
        self.aplicar_efectos_especiales(efectos, escalado)
        self.verificar_combinaciones_especiales()        
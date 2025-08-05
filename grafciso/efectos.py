class Efecto:
    def __init__(self, potencia, duracion: int = 3,):
        self.duracion = duracion
        self.potencia = potencia
        self.turnos_restantes = duracion

    def aplicar(self):
        pass

    def des_aplicar(self):
        pass

# ELEMENTALES:
class Fuego(Efecto):# damage por turno

    def aplicar(self,enemigo):  
        if "fuego" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("fuego")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "fuego" in enemigo.efectos_activos:
            damage = int(self.potencia * 2)
            enemigo.vida -= damage
            self.turnos_restantes -= 1 
            print(f"{enemigo.nombre} recibió {damage} de daño por quemadura")
        
        
        elif "fuego" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("fuego")
            print(f"{enemigo.nombre} dejo de estar quemado")

    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("fuego")
        print(f"{enemigo.nombre} dejo de estar quemado")            

class Rayo(Efecto):# en area
    def aplicar(self, objetivo):
        if isinstance(objetivo, list):  # Para daño en área

            for enemigo in objetivo:
                if enemigo.vivo():
                    daño = int(8 * self.potencia)
                    enemigo.vida -= daño
                    print(f"{enemigo} recibio {daño} de rayo")  
        else:
            if objetivo.vivo():
                    daño = int(12 * self.potencia)
                    objetivo.vida -= daño
                    print(f"{objetivo.nombre} recibio {daño} de rayo")               

class Hielo(Efecto):#debuff

    def aplicar(self,enemigo):  
        if "hielo" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("hielo")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "hielo" in enemigo.efectos_activos:
            damage = int(self.potencia * 2)
            enemigo.velocidad -= damage
            self.turnos_restantes -= 1  # Reducir turnos restantes
            if self.turnos_restantes==self.duracion-1:
                print(f"{enemigo.nombre} bajo su vel {damage} por congelamiento")
        
        
        elif "hielo" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("hielo")
            print(f"{enemigo.nombre} dejo de estar congelado")
            enemigo.velocidad += damage

    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("hielo")
        print(f"{enemigo.nombre} dejo estar congelado")            
# OTRAS:
class Sangrado(Efecto):# damage por turno

    def aplicar(self,enemigo):  
        if "sangrado" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("sangrado")
        
    def actualizar(self,enemigo):        

        if  "sangrado" in enemigo.efectos_activos:
            damage = int(self.potencia * 5)
            enemigo.vida -= damage 
            print(f"{enemigo.nombre} recibió {damage} de daño por sangrado")

    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("sangrado")
        print(f"{enemigo.nombre} dejo de sangrar")

class Curacion(Efecto):

    def aplicar(self,enemigo):  
        if "regeneracion" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("regeneracion")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "regeneracion" in enemigo.efectos_activos:
            damage = int(self.potencia * 2)
            enemigo.vida += damage
            self.turnos_restantes -= 1  # Reducir turnos restantes
            print(f"{enemigo.nombre} recibió {damage} de vida por sanacion")
        
        # Si no hay turnos restantes, eliminar el efecto (si existe)
        elif "regeneracion" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("regeneracion")
            print(f"{enemigo.nombre} dejo de estar quemado")

    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("regeneracion")
        print(f"{enemigo.nombre} dejo de estar sanandose") 

class Veneno(Efecto):# damage por turno

    def aplicar(self,enemigo):  
        if "veneno" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("veneno")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "veneno" in enemigo.efectos_activos:
            damage = int(self.potencia * 2)
            enemigo.vida -= damage
            self.turnos_restantes -= 1  # Reducir turnos restantes
            print(f"{enemigo.nombre} recibió {damage} de daño por envenenamiento")
        
        # Si no hay turnos restantes, eliminar el efecto (si existe)
        elif "veneno" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("veneno")
            print(f"{enemigo.nombre} dejo de estar envenenado") 


    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("veneno")
        print(f"{enemigo.nombre} dejo estar envenenado")                
# VACIO:
class Oscuridad(Efecto):


    def aplicar(self,enemigo):  
        if "oscuridad" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("oscuridad")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "oscuridad" in enemigo.efectos_activos:
            damage = int(self.potencia * 2)
            enemigo.velocidad -= damage
            enemigo.fuerza -= damage
            enemigo.inteligencia -= damage
            enemigo.fe -= damage
            enemigo.defensa -= damage
            self.turnos_restantes -= 1  # Reducir turnos restantes
            
            if self.turnos_restantes==self.duracion:
                print(f"{enemigo.nombre} bajo sus stats {damage} por oscuridad")
        
        # Si no hay turnos restantes, eliminar el efecto (si existe)
        elif "oscuridad" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("oscuridad")
            print(f"{enemigo.nombre} dejo estar en las tinieblas")


    def des_aplicar(self,enemigo):
        enemigo.efectos_activos.remove("oscuridad")
        print(f"{enemigo.nombre} dejo estar en las tinieblas")          

class Abismo(Efecto):


    def aplicar(self,enemigo):  
        if "abismo" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("abismo")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "abismo" in enemigo.efectos_activos:
            damage = int(self.potencia * 3)
            enemigo.vida -= damage*2
            if self.turnos_restantes==self.duracion:
                enemigo.velocidad -= damage
                enemigo.fuerza -= damage
                enemigo.inteligencia -= damage
                enemigo.fe -= damage
                enemigo.defensa -= damage
                self.turnos_restantes -= 1  # Reducir turnos restantes
            
            if self.turnos_restantes==self.duracion:
                print(f"{enemigo.nombre} bajo sus stats {damage*2} por abismo")
            print(f"y recibio {damage} de damage")
        
        # Si no hay turnos restantes, eliminar el efecto (si existe)
        elif "abismo" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("abismo")
            print(f"{enemigo.nombre} dejo de estar en el abismo")
            enemigo.velocidad += damage
            enemigo.fuerza += damage
            enemigo.inteligencia += damage
            enemigo.fe += damage
            enemigo.defensa += damage

class Luz(Efecto):

    def aplicar(self,enemigo):  
        if "luz" not in enemigo.efectos_activos:
            enemigo.efectos_activos.append("luz")
        
    def actualizar(self,enemigo):        

        if self.turnos_restantes > 0 and "luz" in enemigo.efectos_activos:
            damage = int(self.potencia * 3)
            enemigo.vida += damage*2
            if self.turnos_restantes==self.duracion:
                enemigo.velocidad += damage
                enemigo.fuerza += damage
                enemigo.inteligencia += damage
                enemigo.fe += damage
                enemigo.defensa += damage
                self.turnos_restantes -= 1  # Reducir turnos restantes
            
            if self.turnos_restantes==self.duracion:
                print(f"{enemigo.nombre} subio sus stats {damage*2} por estar iluminado")
            print(f"y recibio {damage} de damage")
        
        # Si no hay turnos restantes, eliminar el efecto (si existe)
        elif "luz" in enemigo.efectos_activos:
            enemigo.efectos_activos.remove("luz")
            enemigo.velocidad -= damage
            enemigo.fuerza -= damage
            enemigo.inteligencia -= damage
            enemigo.fe -= damage
            enemigo.defensa -= damage
            print(f"{enemigo.nombre} dejo de estar iluminado")


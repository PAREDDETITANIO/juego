class Habilidad:
    def __init__(self, nombre, descripcion, coste, tipo, funcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.coste = coste  # Coste de mana, rezo, etc.
        self.tipo = tipo    # ataque / curación / buff
        self.funcion = funcion  # una función que define el efecto

    def usar(self, usuario, objetivo):
        return self.funcion(usuario, objetivo)


def estocada(jugador,enemigo):
        
    jugador.mana -=20
    print("\n¡Estocada!")
    damage = jugador.fuerza_total() * 1.5 - enemigo.defensa
    enemigo.vida -= max(damage, 0)
    if enemigo.vivo():
        print("\ndamage de",jugador.nombre,":",damage)
        print("vida de",enemigo.nombre,":",enemigo.vida)
    else:
        print("\ndamage de",jugador.nombre,":",damage)
        print("vida de",enemigo.nombre,0)
        enemigo.matar()
import classes as cl
import random as r
import armas as a
import grafciso.efectos as ef
# Constantes
MAX_PISOS = 100

def validar_input(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"\nError: Ingresa un número entre {minimo} y {maximo}")
        except ValueError:
            print("\nError: Debes ingresar un número entero válido")

def menu_turno():
    print("\n1. Atacar")
    print("2. Curar")
    print("3. Inventario")
    print("4. Stats")

def menu_atac():
    print("\n1. Basico")
    print("2. hab1")
    print("3. hab2")
    print("4. Ult")

def menu_inv():
    print("\n1. Ver inventario")    
    print("2. Cambiar arma")      
    print("3. Cambiar armadura")

def menu_clase():
    print("\nElige tu clase:")
    print("1. Guerrero")
    print("2. Mago")
    print("3. Templario")
    print("4. Cientifico")
    print("5. Samurai")

def levelear_enemigo(enemigo, piso_actual):
    incremento = max(1, int(r.gauss(0 + piso_actual*0.5, 3)))  
    incremento = min(10 + piso_actual, incremento)
    for _ in range(incremento - 1):
        enemigo.levelup()

def seleccionar_clase():
    while True:
        name=input("Elije Un Nombre:")
        menu_clase()
        entrada = input("Opción: ")
        print(f" Has ingresado: {entrada}")  
        
        try:
            opcion = int(entrada)
            if 1 <= opcion <= 5:
                return [cl.Guerrero, cl.Mago, cl.Templario, cl.Cientifico, cl.Samurai][opcion-1](name)
            print("Error: Debe ser entre 1 y 5")
        except ValueError:
            print("Error: Debes ingresar SOLO números (1-5)")




def dar_recompensa(jugador):
    recompensas = {
        cl.Guerrero: a.Arma_g,
        cl.Mago: a.Arma_m,
        cl.Templario: a.Arma_t,
        cl.Cientifico: a.Arma_c
    }
    
    for clase, clase_arma in recompensas.items():
        if isinstance(jugador, clase):
            nueva_arma = clase_arma(
                lvl_P=jugador.lvl,
                suerte=jugador.suerte
            )
            jugador.pick(nueva_arma)
            break

def encontrar_pocion(jugador):
    if r.random() < 0.3:  
        tipo = r.choices(population=[0, 1, 2], weights=[0.6, 0.3, 0.1], k=1)[0]
        jugador.inventario["pociones"][tipo] += 1

        nombres = ["chica", "mediana", "grande"]
        print(f"\n¡Encontraste una poción {nombres[tipo]}!")

        print(f"Pociones chicas: {jugador.inventario['pociones'][0]}")
        print(f"Pociones medianas: {jugador.inventario['pociones'][1]}")
        print(f"Pociones grandes: {jugador.inventario['pociones'][2]}")

def curar_jugador(jugador, cantidad_pociones):
    """Cura al jugador después de vencer un piso"""
    curacion = 50
    if jugador.vida_maxima < jugador.vida + curacion:
        curacion = jugador.vida_maxima - jugador.vida
    
    jugador.vida += curacion
    print(f"Te curaste: {curacion} HP")
    
    # Devolver si se usó poción
    return cantidad_pociones - 1 if curacion > 0 else cantidad_pociones

def enemigo_ataque():
    pass

def generar_enemigos(piso_actual):

    if piso_actual < 10:
        cantidad = 1
    elif piso_actual < 20:
        cantidad = r.choices([1, 2], weights=[0.7, 0.3])[0]
    else:
        cantidad = r.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
    
    enemigos = []
    for i in range(cantidad):
        enemigo = cl.Enemigo(f"FABIAN {piso_actual}-{i+1}")
        levelear_enemigo(enemigo, piso_actual)
        enemigos.append(enemigo)
    
    return enemigos

def seleccionar_enemigo(enemigos):

    vivos = [e for e in enemigos if e.vivo()]
    if not vivos:
        return None
    
    if len(vivos) == 1:
        print(f"\nAtacando automáticamente a {vivos[0].nombre}")
        return vivos[0]
    
    print("\nEnemigos disponibles:")
    for i, enemigo in enumerate(vivos, 1):
        print(f"{i}. {enemigo.nombre} (Vida: {enemigo.vida}/{enemigo.vida_maxima})")
    
    while True:
        try:
            seleccion = int(input("\nSelecciona un enemigo: ")) - 1
            if 0 <= seleccion < len(vivos):
                return vivos[seleccion]
            print("Número inválido. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número.")

def turno_enemigos(jugador, enemigos):

    for enemigo in enemigos:
        if enemigo.vivo():
            enemigo.ataque(jugador)
            if not jugador.vivo():
                break  

def aplicar_efectos(jugador, enemigo):

    if not enemigo.vivo() or "arma" not in jugador.equipo:
        return

    efectos_instancias = {}

    for efecto in jugador.equipo["arma"].efectos_activos:
        potencia = int(jugador.equipo["arma"].lvl * 0.1)

        if efecto == "fuego":
            efectos_instancias["fuego"] = ef.Fuego(potencia)
            efectos_instancias["fuego"].aplicar(enemigo)
        elif efecto == "rayo":
            efectos_instancias["rayo"] = ef.Rayo(potencia)
            efectos_instancias["rayo"].aplicar(enemigo)
        elif efecto == "hielo":
            efectos_instancias["hielo"] = ef.Hielo(potencia)
            efectos_instancias["hielo"].aplicar(enemigo)


    if "fuego" in enemigo.efectos_activos and "fuego" in efectos_instancias:
        efectos_instancias["fuego"].actualizar(enemigo)
    if "hielo" in enemigo.efectos_activos and "hielo" in efectos_instancias:
        efectos_instancias["hielo"].actualizar(enemigo)
   

# Inicio del juego

jugador = seleccionar_clase()
pociones = 1


for piso_actual in range(1, MAX_PISOS + 1):
    enemigos = generar_enemigos(piso_actual)
    print(f"\n=== PISO {piso_actual} ===")
    jugador.atributos()
    for enemigo in enemigos:
        enemigo.atributos()

    turno = 1
    while jugador.vivo() and any(e.vivo() for e in enemigos):
        print("\nTurno:", turno)
        



        menu_turno()
        opcion = validar_input("\nSelecciona una opción: ", 1, 4)

        if opcion == 1:
            menu_atac()
            opcion1 = validar_input("\nElige tipo de ataque: ", 1, 4)

            # Selección automática si hay un solo enemigo
            enemigo_objetivo = seleccionar_enemigo(enemigos)
            if not enemigo_objetivo:
                break  # No hay enemigos vivos

            if jugador.velocidad_total() >= enemigo_objetivo.velocidad_total():
                # Jugador ataca primero
                if opcion1 == 1:
                    jugador.ataque(enemigo_objetivo)
                    aplicar_efectos(jugador,enemigo)

                       
                elif opcion1 == 2 and jugador.get_mana() >= 20:
                    jugador.hab_1(enemigo_objetivo)
                elif opcion1 == 3 and jugador.get_mana() >= 40:
                    jugador.hab_2(enemigo_objetivo)
                elif opcion1 == 4 and jugador.get_mana() >= 100:
                    jugador.ult(enemigo_objetivo)
                else:
                    print("\nMana Insuficiente")
                    continue
                
                # Todos los enemigos vivos contraatacan
                if any(e.vivo() for e in enemigos):
                    turno_enemigos(jugador, enemigos)
            else:
                # Enemigos atacan primero
                turno_enemigos(jugador, enemigos)
                if jugador.vivo():  # Solo ataca si sobrevive
                    if opcion1 == 1:
                        jugador.ataque(enemigo_objetivo)
                        aplicar_efectos(jugador,enemigo)
                    elif opcion1 == 2 and jugador.get_mana() >= 20:
                        jugador.hab_1(enemigo_objetivo)
                    elif opcion1 == 3 and jugador.get_mana() >= 40:
                        jugador.hab_2(enemigo_objetivo)
                    elif opcion1 == 4 and jugador.get_mana() >= 100:
                        jugador.ult(enemigo_objetivo)
                    else:
                        print("\nMana Insuficiente")
                        continue

            turno += 1

      
        elif opcion == 2:
            jugador.ver_invent(3)
            tipo = validar_input("\nElige poción (1-3): ", 1, 3)
            jugador.curar(tipo)
            

        elif opcion == 3:
            menu_inv()
            opcion2 = validar_input("\nElige opción de inventario (1-3): ", 1, 3)  
            if opcion2 == 1:
                print("\n1. Armas:")
                print("2. Armaduras:")
                print("3. Pociones:")
                opcion3 = validar_input("\nElige categoría a ver (1-3): ", 1, 3)
                jugador.ver_invent(opcion3)
            elif opcion2 == 2:
                jugador.equipar_arma()
            elif opcion2 == 3:
                jugador.equipar_armadura()
            
           

        elif opcion == 4:  # Stats
            jugador.atributos()
            print("\n--- EFECTOS ACTIVOS ---")
            print(f"Jugador: {', '.join([str(ef) for ef in jugador.efectos_activos]) or 'Ninguno'}")
            
            for i, enemigo in enumerate(enemigos, 1):
                if enemigo.vivo():
                    enemigo.atributos()
                    print(f"Enemigo {i}: {', '.join([str(ef) for ef in enemigo.efectos_activos]) or 'Ninguno'}")

    if jugador.vivo() and not any(e.vivo() for e in enemigos):
        dar_recompensa(jugador)
        encontrar_pocion(jugador)
        jugador.expc([e.lvl for e in enemigos]) 
        curar_jugador(jugador, pociones)                

if jugador.vivo() and piso_actual == MAX_PISOS:
    print("\n🎉 ¡Felicidades! ¡Has completado todos los pisos! 🎉")
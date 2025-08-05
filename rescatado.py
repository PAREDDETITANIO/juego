def preguntar_raza(self):
        print("\nElige una raza:")
        print("1. Humano")
        print("2. Elfo")
        print("3. Demonio")
        print("4. Orco")
        print("5. Dracónido\n")      

        while True:
            try:
                eleccion = int(input("Ingresa el número de la raza: "))
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
                    print("\nOpción no válida. Intenta de nuevo.")
            except ValueError:
                print("\nPor favor, ingresa un número.")
        self.aplicar_bono_racial()




def atributos(self):
        print(f"\n{self.nombre}:")
        print(f"Raza: {self.raza}")
        print(f"Nivel: {self.lvl}")
        print(f"Vida: {self.vida} / {self.vida_maxima}")
        print(f"{self.recurso_nombre}: {self.mana} / {self.mana_maxima}")
        print(f"Fuerza: {self.fuerza}")
        print(f"Inteligencia: {self.inteligencia} iq")
        print(f"Fe: {self.fe}")
        print(f"Defensa: {self.defensa}")
        print(f"Velocidad: {self.velocidad}")
        print(f"Suerte: {self.suerte}")
        print()
        print(f"Altura: {self.altura}cm")
        print(f"Peso: {self.peso}kg")



class Vehiculos:
    def __init__(self, marca, modelo, año):
        self._marca = None
        self.set_marca(marca)
        self.modelo = modelo
        self.año = año
    def get_marca(self):
        return self._marca
  
    def set_marca(self, marca):
        try:
            assert isinstance(marca, str), "La marca debe ser una cadena de texto (str)."
            self._marca = marca
        except AssertionError as e:
            print(f"aqui se muestra el error del assert: {e}")
        finally:
            print("aqui se muestra el finally.")  
    marca=property(get_marca,set_marca) 
    def informacion(self):
        return f'La marca es {self.marca}, modelo: {self.modelo} del año: {self.año}.'


class Moto(Vehiculos):
    def __init__(self, marca, modelo, año, cilindrada):
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada
    
    def arranca(self):
        print("arranca -> ----->")


class Automovil(Vehiculos):
    def __init__(self, marca, modelo, año, llantas):
        super().__init__(marca, modelo, año)
        self.llantas = llantas
    
    def arranca(self):
        print("arranca -> ----->")


class Bicicleta(Vehiculos):    
    def __init__(self, marca, modelo, año, numero_cadena):
        super().__init__(marca, modelo, año)
        self.numero_cadena = numero_cadena
    
    def pedalea(self):
        print("avanza -> ----->")
    
    def frena(self):
        print("frena <---")    


class Motor:
    def __init__(self, cilindrada, tipo_combustible):
        self.cilindrada = cilindrada
        self.tipo_combustible = tipo_combustible
    
    def arranca(self):
        print("arranca")


class Electrico:
    def __init__(self, capacidad_combustible):
        self.capacidad_combustible = capacidad_combustible
    
    def cargar_bateria(self):
        print("cargando bateria")


# Herencia múltiple
class Automovil_Electrico(Automovil, Electrico):
    def __init__(self, marca, modelo, año, llantas, capacidad_combustible):
        Automovil.__init__(self, marca, modelo, año, llantas)
        Electrico.__init__(self, capacidad_combustible)


class Motocicleta_Electrica(Moto, Electrico):
    def __init__(self, marca, modelo, año, cilindrada, capacidad_combustible,velocidad):
        Moto.__init__(self, marca, modelo, año, cilindrada)
        Electrico.__init__(self, capacidad_combustible)
        self.velocidad=velocidad
    def frena(self,freno):
        try:
            assert (freno>0)

        except AssertionError:
            print('aqui se muestra el error del assert')
        except:
            print("aui se muesttra el error general")
        else:
            velocidad=velocidad-frenos
            print('velocidad se redujo a --->',velocidad)
            


class Automovil_Motor(Automovil, Motor):
    def __init__(self, marca, modelo, año, llantas, cilindrada, tipo_combustible):
        Automovil.__init__(self, marca, modelo, año, llantas)
        Motor.__init__(self, cilindrada, tipo_combustible)

automovil_motor = Motocicleta_Electrica(6, "Model S", 2020, 4,6,30)
print(automovil_motor.informacion())
automovil_motor.arranca()
automovil_motor.frena(0)
automovil_motor.frena('e')
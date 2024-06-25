class publicacion:
    titulo_publicacion=[]
    def __init__(self,titulo,autor,anio_publicacion):
        self.set_titulo(titulo)
        self.set_autor(autor)
        self.set_anio(anio_publicacion)
        publicacion.titulo_publicacion.append(titulo)
    @classmethod
    def existe_titulo(cls,titulo):
        try:
            if titulo in cls.titulo_publicacion:
                return f"el libro existe"
        except ValueError:
            return f"el libro no existe ¡¡Error!!"
    def get_titulo(self):
        return self.__titulo
    def set_titulo(self,titulo):
        self.__titulo=titulo
    titulo=property(get_titulo,set_titulo)
    def get_autor(self):
        return self.__autor
    def set_autor(self,autor):
        self.__autor=autor
    autor=property(get_autor,set_autor)
    def get_anio(self):
        return self.__anio
    def set_anio(self,anio):
        if not self.validar_fecha(anio):
            raise ValueError("la fecha no es valida")
        self.__anio=anio
    anio=property(get_anio,set_anio) 
    def info(self):
        return f"el libro {self.titulo},escrito por{self.autor},con fecha{self.anio}"

    @staticmethod
    def validar_fecha(anio):
        try:
            fecha=int(anio)
            return fecha>=0
        except ValueError:
            return False



class libro(publicacion):
    def __init__(self,titulo,autor,anio_publicacion,numeros_paginas):
        super().__init__(titulo,autor,anio_publicacion)
        self.set_numero(numeros_paginas)
    def get_numero(self):
        return self.__numero
    def set_numero(self, numero):
        self.__numero=numero
    numero=property(get_numero,set_numero)
    def info_libro(self):
        return f"el libro {self.titulo},escrito por{self.autor},con fecha{self.anio},con un numero de paginas {self.numero}"

class periodico:
    def __init__(self,frecuencia):
        self.set_frecuencia(frecuencia)
    def get_frecuencia(self):
        return self.__frecuencia
    def set_frecuencia(self, frecuencia):
        self.__frecuencia=frecuencia
    frecuencia=property(get_frecuencia,set_frecuencia)

class revista(publicacion,periodico):
    def __init__(self,titulo,autor,anio_publicacion,frecuencia,numero_edicion):
        publicacion.__init__(self,titulo,autor,anio_publicacion)
        periodico.__init__(self,frecuencia)
        self.numero_edicion=numero_edicion  
    def info_revista(self):
        return f"el libro {self.titulo},escrito por{self.autor},con fecha{self.anio},con frecuencia: {self.frecuencia} , edicion:{self.numero_edicion}"
    
def verificar_tipo():
    if isinstance(publicacion,libro):
        print("es un libro")
    elif isinstance(publicacion,revista):
        print("es una revista")
    else:
        print("no hay esa categoria")

libro1=revista("got","edu","2020",20,18)
print(libro1.info_revista())


print(libro1.existe_titulo("lol"))
from usuario import Usuario

class Padre(Usuario):
    def __init__(self, id_usuario, nombre, pin_seguridad):
        # Llama a Usuario forzando el rol "PADRE"
        super().__init__(id_usuario, nombre, "PADRE", pin_seguridad)
from usuario import Usuario

class Hijo(Usuario):
    def __init__(self, id_usuario, nombre, pin_seguridad):
        # Llama a Usuario forzando el rol "HIJO"
        super().__init__(id_usuario, nombre, "HIJO", pin_seguridad)
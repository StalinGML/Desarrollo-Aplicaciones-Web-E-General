from flask_login import UserMixin


class Usuario(UserMixin):

    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

    @property
    def nombre(self):
        return self.usuario
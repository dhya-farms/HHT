from django.contrib.auth import get_user_model

from app.utils.controllers import Controller

UserModel = get_user_model()


class UserController(Controller):
    def __init__(self):
        super().__init__(model=UserModel)

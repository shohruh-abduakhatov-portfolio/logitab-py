from enum import Enum


class WebEnum(Enum):
    def __str__(self):
        return str(self.value)


    def __int__(self):
        return int(self.value)


    def __float__(self):
        return float(self.value)


    def __get__(self, instance, owner):
        return self.value


class UserRole(WebEnum):
    ADMIN = "admin"
    DRIVER = "driver"
    OPERATOR = "operator"

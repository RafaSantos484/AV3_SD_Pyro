import random
import time


def id_eh_valido(id_sensor: str):
    err_msg = None
    if id_sensor == "":
        err_msg = "Digite um identificador não vazio"
    if len(id_sensor) > 20:
        err_msg = "O identificador deve ter, no máximo, 20 caracteres"

    if err_msg:
        print(err_msg)
        return False
    return True


def simular_delay():
    time.sleep(random.uniform(5.0, 12.0))


def obter_dado():
    return format(random.uniform(30.0, 60.0), ".2f")

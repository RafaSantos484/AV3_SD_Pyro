import random
import time


def dormir(tempo: float):
    time.sleep(tempo)


def dormir_tempo_aleatorio(tempo_min: float, tempo_max: float):
    time.sleep(random.uniform(tempo_min, tempo_max))


def testar_probabilidade(probabilidade: float):
    return random.random() < probabilidade


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
    dormir_tempo_aleatorio(5.0, 12.0)


def obter_dado():
    return format(random.uniform(30.0, 60.0), ".2f")

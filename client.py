import Pyro4 as Pyro
import utils

ns = Pyro.locateNS()
uri = ns.lookup("server")
obj = Pyro.Proxy(uri)

id_sensor = ""
while True:
    id_sensor = input("Digite o identificador do sensor: ")
    if utils.id_eh_valido(id_sensor):
        if obj.inserir_sensor(id_sensor):
            break
        else:
            print("Identificador já usado")

print(f"Sensor {id_sensor} registrado")

while True:
    utils.simular_delay()

    obj.registrar_dado(utils.obter_dado(), id_sensor)

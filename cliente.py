import Pyro4 as Pyro
import threading
import utils

ns = Pyro.locateNS()
uri_principal = ns.lookup("servidor_principal")
uri_reserva = ns.lookup("servidor_reserva")
servidor_principal = Pyro.Proxy(uri_principal)
servidor_reserva = Pyro.Proxy(uri_reserva)

id_sensor = ""
while True:
    id_sensor = input("Digite o identificador do sensor: ")
    if utils.id_eh_valido(id_sensor):
        inseriu_sensor = False
        try:
            inseriu_sensor = servidor_principal.inserir_sensor(id_sensor)
        except:
            print("Servidor principal inoperante. Aguardando resposta do servidor secundário")
            inseriu_sensor = servidor_reserva.inserir_sensor(id_sensor)
        finally:
            if inseriu_sensor:
                break
            else:
                print("Identificador já usado")

print(f"Sensor {id_sensor} registrado")

while True:
    utils.simular_delay()

    dado = utils.obter_dado()
    try:
        servidor_principal.registrar_dado(dado, id_sensor)
    except:
        print("Servidor principal inoperante. Enviando dado para o servidor secundário")
        servidor_reserva.registrar_dado(dado, id_sensor)

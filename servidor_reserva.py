import Pyro4 as Pyro
import threading
from dado import Dado
import utils

ns = Pyro.locateNS()
uri_principal = ns.lookup("servidor_principal")
servidor_principal = Pyro.Proxy(uri_principal)
ev_serv_princ_operante = threading.Event()


@Pyro.expose
class ServidorReserva:
    def __init__(self):
        self.dados = []
        threading.Thread(target=thread_enviar_dados, args=[self]).start()

    # Aguarda servidor principal voltar a ficar operante para validar novo sensor
    def inserir_sensor(self, id_sensor: str):
        print(f"Aguardando servidor principal voltar a ficar operante para tentar inserir sensor {id_sensor}")
        while not servidor_principal.ping():
            utils.dormir(0.1)

        print(f"Servidor principal voltou a ficar operante. Tentando inserir sensor {id_sensor}")
        return servidor_principal.inserir_sensor(id_sensor)

    def registrar_dado(self, dado: str, id_sensor: str):
        print(f"Registrando dado do sensor {id_sensor}")
        self.dados.append(Dado(dado, id_sensor))


# Envia dados para o servidor principal que ele não recebeu enquanto estava inoperante
def thread_enviar_dados(servidor: ServidorReserva):
    while True:
        while len(servidor.dados) == 0:
            utils.dormir(1.0)

        while not servidor_principal.ping():
            utils.dormir(0.1)

        print("Enviando dados para o servidor principal")
        dados_str = "["
        for dado in servidor.dados:
            dados_str += f"Dado('{dado.info}','{dado.id_sensor}'),"
        dados_str += "]"
        servidor_principal.registrar_dados_serv_reserva(dados_str)
        servidor.dados = []


daemon = Pyro.Daemon()
uri = daemon.register(ServidorReserva())
ns = Pyro.locateNS()
ns.register("servidor_reserva", uri)
print(uri)

daemon.requestLoop()

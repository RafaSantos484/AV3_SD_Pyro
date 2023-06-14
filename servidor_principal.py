import Pyro4 as Pyro
import threading
from dado import Dado
import utils


@Pyro.expose
class ServidorPrincipal:
    def __init__(self):
        self.sensores = []
        self.dados = []
        self.estah_inoperante = False
        threading.Thread(target=thread_simular_inoperante, args=[self]).start()

    def ping(self):
        if self.estah_inoperante:
            utils.dormir(3.0)
            return False

        return True

    def printar_dados(self):
        if self.estah_inoperante:
            utils.dormir(2.0)
            raise Exception("Servidor inoperante")

        i = 0
        for dado in self.dados:
            print(f"{i}: {dado.info}({dado.id_sensor})")
            i += 1
        print("=====================================")

    def inserir_sensor(self, id_sensor: str):
        if self.estah_inoperante:
            utils.dormir(2.0)
            raise Exception("Servidor inoperante")

        if id_sensor in self.sensores:
            return False

        self.sensores.append(id_sensor)
        return True

    def registrar_dado(self, dado: str, id_sensor: str):
        if self.estah_inoperante:
            utils.dormir(2.0)
            raise Exception("Servidor inoperante")

        self.dados.append(Dado(dado, id_sensor))
        self.printar_dados()

    def registrar_dados_serv_reserva(self, dados_str: str):
        print("Inserindo dados do servidor reserva enquanto estava inoperante")
        dados = eval(dados_str)
        self.dados += dados
        self.printar_dados()


def thread_simular_inoperante(servidor: ServidorPrincipal):
    while True:
        # 30% de chance de ficar inoperante em intervalos aleatórios de tempo
        ficou_inoperante = utils.testar_probabilidade(0.3)
        if ficou_inoperante:
            servidor.estah_inoperante = True
            print("Servidor ficou inoperante")
            # Fica inoperante por 15 a 20 segundos
            utils.dormir_tempo_aleatorio(15.0, 20.0)
            servidor.estah_inoperante = False
            print("Servidor voltou a ficar operante")
            # Fica um mínimo de 5 segundos operante até pode ficar inoperante novamente
            utils.dormir(5.0)
        else:
            utils.dormir_tempo_aleatorio(5.0, 8.0)


daemon = Pyro.Daemon()
uri = daemon.register(ServidorPrincipal())
ns = Pyro.locateNS()
ns.register("servidor_principal", uri)
print(uri)

daemon.requestLoop()

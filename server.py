import Pyro4 as Pyro

from dado import Dado


@Pyro.expose
class Server:
    def __init__(self):
        self.sensores = []
        self.dados = []

    def inserir_sensor(self, id_sensor: str):
        if id_sensor in self.sensores:
            return False

        self.sensores.append(id_sensor)
        return True

    def registrar_dado(self, dado: float, id_sensor: str):
        self.dados.append(Dado(dado, id_sensor))

        i = 0
        for dado in self.dados:
            print(f"{i}: {dado.info}({dado.id_sensor})")
            i += 1
        print("=====================================")


daemon = Pyro.Daemon()

uri = daemon.register(Server())
ns = Pyro.locateNS()
ns.register("server", uri)
print(uri)

daemon.requestLoop()

from peer import Peer

class PeerManager:
    def __init__(self):
        self.peers = {}

    def adicionar_peer(self, endereco_porta, status="OFFLINE"):
        if endereco_porta not in self.peers:
            self.peers[endereco_porta] = Peer(endereco_porta, status)
            print(f"Adicionando novo peer {endereco_porta} status {status}")
        else:
            self.atualizar_status(endereco_porta, status)

    def atualizar_status(self, endereco_porta, novo_status):
        if endereco_porta in self.peers:
            self.peers[endereco_porta].status = novo_status
            print(f"Atualizando peer {endereco_porta} status {novo_status}")

    def listar_peers(self):
        return list(self.peers.values())

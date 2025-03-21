class Peer:
    def __init__(self, endereco_porta: str, status="OFFLINE"):
        self.endereco_porta = endereco_porta
        self.status = status

    def __repr__(self):
        return f"<Peer {self.endereco_porta} - {self.status}>"

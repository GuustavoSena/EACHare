class Clock:
    def __init__(self):
        self.valor = 0

    def incrementar(self):
        self.valor += 1
        print(f"=> Atualizando relogio para {self.valor}")
        return self.valor

    def atualizar_ao_receber(self):
        self.valor += 1
        print(f"=> Atualizando relogio para {self.valor}")

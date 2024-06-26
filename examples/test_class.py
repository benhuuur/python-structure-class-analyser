# Definição da classe Produto
class Produto:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = "nome"
        self.preco = 2

    def exibir_informacoes(self):
        print(f"Código: {self.codigo}")
        print(f"Nome: {self.nome}")
        print(f"Preço: R${self.preco:.2f}")

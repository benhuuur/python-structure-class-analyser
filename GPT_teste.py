# Definição da classe Produto
class Produto:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
    
    def exibir_informacoes(self):
        print(f"Código: {self.codigo}")
        print(f"Nome: {self.nome}")
        print(f"Preço: R${self.preco:.2f}")

# Definição da classe Cliente
class Cliente:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
    
    def exibir_dados(self):
        print(f"Nome do Cliente: {self.nome}")
        print(f"E-mail do Cliente: {self.email}")

# Definição da classe Pedido
class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.produtos = []
    
    def adicionar_produto(self, produto):
        self.produtos.append(produto)
    
    def calcular_total(self):
        total = 0
        for produto in self.produtos:
            total += produto.preco
        return total
    
    def exibir_pedido(self):
        self.cliente.exibir_dados()
        print("Produtos no pedido:")
        for produto in self.produtos:
            produto.exibir_informacoes()
        print(f"Total do pedido: R${self.calcular_total():.2f}")

# Exemplo de uso das classes
if __name__ == "__main__":
    # Criando alguns produtos
    produto1 = Produto(1, "Camiseta", 29.99)
    produto2 = Produto(2, "Calça Jeans", 79.90)
    
    # Criando um cliente
    cliente1 = Cliente("João", "joao@email.com")
    
    # Criando um pedido para o cliente
    pedido1 = Pedido(cliente1)
    
    # Adicionando produtos ao pedido
    pedido1.adicionar_produto(produto1)
    pedido1.adicionar_produto(produto2)
    
    # Exibindo o pedido
    pedido1.exibir_pedido()

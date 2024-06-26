class Pessoa:
    sobrenome = ""

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def apresentar(self):
        print(f"Olá, eu sou {self.nome} e tenho {self.idade} anos.")


pessoa1 = Pessoa("João", 30)
# pessoa1.apresentar()


class Ser_Vivo ():
    def __init__(self):
        self.exemplo = ''
        self.vivo = True


class Animal(Ser_Vivo):
    def Barulho(self):
        self.exemplo = "la"
        print("sjalkjaksdj")


class Humano(Ser_Vivo, Pessoa):
    animal, animal2 = Animal(), Animal()
    sla = "junin"

    def __init__(self):
        super().__init__()
        self.kaka = "blessed"

    def Barulho(self):
        print("sjalkjaksdj")


pessoa2 = Pessoa("Maria", 25)
# pessoa2.apresentar()

class_name = "ll"

animal = Animal()
animal.Barulho()
print(animal.exemplo)

animal2 = Animal()
print(animal2.exemplo)

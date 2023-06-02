import json


class Node:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo
        self.resp_sim = None
        self.resp_nao = None


class Arvore:
    def jogar(self, el_atual):
        if el_atual.tipo == "animal":
            chute = input("O animal que você pensou é " +
                          el_atual.valor + "? (S/N): ")
            if chute.upper() == "S":
                print("Acertei de novo!")
            else:
                animal = input("Qual animal você pensou? ")
                pergunta = input("Diga uma pergunta cuja resposta é 'sim' para " +
                                 animal + " e 'não' para " + el_atual.valor + ": ")
                novo_animal = Node(animal, "animal")
                nova_pergunta = Node(pergunta, "pergunta")
                resposta = input("Qual seria a resposta para a pergunta '" +
                                 pergunta + "' se o animal fosse " + animal + "? (S/N): ")
                if resposta.upper() == "S":
                    nova_pergunta.resp_sim = novo_animal
                    nova_pergunta.resp_nao = el_atual
                else:
                    nova_pergunta.resp_sim = el_atual
                    nova_pergunta.resp_nao = novo_animal
                return nova_pergunta
        else:
            resposta = input(el_atual.valor + " (S/N): ")
            if resposta.upper() == "S":
                el_atual.resp_sim = self.jogar(el_atual.resp_sim)
            else:
                el_atual.resp_nao = self.jogar(el_atual.resp_nao)
        return el_atual

    def salvar_arvore(self, raiz):
        dados_arvore = self.serializa_arvore(raiz)
        with open("tree.json", "w") as file:
            json.dump(dados_arvore, file)

    def carregar_arvore(self):
        try:
            with open("tree.json", "r") as file:
                dados_arvore = json.load(file)
                return self.deserializa_arvore(dados_arvore)
        except FileNotFoundError:
            return None

    def serializa_arvore(self, node):
        if node is None:
            return None
        return {
            "valor": node.valor,
            "tipo": node.tipo,
            "resp_sim": self.serializa_arvore(node.resp_sim),
            "resp_nao": self.serializa_arvore(node.resp_nao)
        }

    def deserializa_arvore(self, dados):
        if dados is None:
            return None
        node = Node(dados["valor"], dados["tipo"])
        node.resp_sim = self.deserializa_arvore(dados["resp_sim"])
        node.resp_nao = self.deserializa_arvore(dados["resp_nao"])
        return node


def main():
    arvore = Arvore()
    raiz = arvore.carregar_arvore()
    if raiz is None:
        raiz = Node("baleia", "animal")

    while True:
        print("Pense em um animal!")
        raiz = arvore.jogar(raiz)
        arvore.salvar_arvore(raiz)
        jogar_novamente = input("Deseja jogar novamente? (S/N): ")
        if jogar_novamente.upper() != "S":
            break


if __name__ == "__main__":
    main()

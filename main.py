import pickle
import os


class Node:
    def __init__(self, data):
        self.data = data
        self.yes = None
        self.no = None

    def is_animal(self):
        return self.yes is None and self.no is None


class Tree:
    def __init__(self):
        self.root = None

    def start_game(self):
        print("Pense em um animal!")
        self.root = self.play(self.root)

    def play(self, node):
        if node is None:
            animal = input("Qual foi o animal que você pensou? ")
            node = Node(animal)
            self.save_tree()
        else:
            if not node.is_animal():
                p = input(f"É {self.root.data}? ".capitalize())
                if p.lower() == "sim":
                    self.play(node.yes)
                else:
                    self.play(node.no)

            else:
                vocePensou = input(f"Você pensou em {node.data}? (sim/não): ")
                if vocePensou.lower() == "sim":
                    print("Ótimo")
                else:
                    animal = input("Qual foi o animal que você pensou? ")
                    dif = input(
                        f"Diga uma característica de {animal} que é diferente de {node.data}: ")
                    answer = input(
                        f"O(a) {animal} possui essa característica (sim/não): ")
                    node = Node(dif)
                    node.data = dif
                    if answer.lower() == "sim":
                        node.yes = Node(animal)
                        node.no = Node(node.data)
                    else:
                        node.yes = Node(node.data)
                        node.no = Node(animal)
        return node

    def save_tree(self):
        with open("tree.pkl", 'wb') as file:
            pickle.dump(self.root, file)

    def load_tree(self):
        if os.path.isfile("tree.pkl"):
            with open("tree.pkl", 'rb') as file:
                self.root = pickle.load(file)


if __name__ == "__main__":
    tree = Tree()
    tree.load_tree()
    tree.start_game()
    tree.save_tree()

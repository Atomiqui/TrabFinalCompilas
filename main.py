import os

def leGramatica():
    with open("gramatica.txt") as file:
        return file.read()

def main():
    gramatica = leGramatica()
    print(gramatica)

main()
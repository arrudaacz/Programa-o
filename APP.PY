from flask import Flask, request, jsonify
from flask_cors import CORS
from abc import ABC, abstractmethod
import random

app = Flask(__name__)
CORS(app)

class Disciplina(ABC):
    def __init__(self, nome):
        self.nome = nome
        self.dificuldade = 1
        self.historico = []

    @abstractmethod
    def gerar_exercicio(self):
        pass

    @abstractmethod
    def corrigir(self, exercicio, resposta):
        pass

    def registrar_resposta(self, correto):
        self.historico.append(correto)
        self.ajustar_dificuldade()

    def ajustar_dificuldade(self):
        if len(self.historico) < 3:
            return

        ultimos = self.historico[-3:]

        if ultimos == [True, True, True] and self.dificuldade < 3:
            self.dificuldade += 1

        if ultimos == [False, False, False] and self.dificuldade > 1:
            self.dificuldade -= 1


class Matematica(Disciplina):
    def __init__(self):
        super().__init__("Matemática")

    def gerar_exercicio(self):
        if self.dificuldade == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
            return (f"Quanto é {a} + {b}?", str(a + b))

        elif self.dificuldade == 2:
            a, b = random.randint(5, 20), random.randint(2, 10)
            return (f"Quanto é {a} x {b}?", str(a * b))

        else:
            a = random.randint(2, 12)
            return (f"Quanto é {a}²?", str(a * a))

    def corrigir(self, exercicio, resposta):
        return resposta == exercicio[1]


class Portugues(Disciplina):
    def __init__(self):
        super().__init__("Português")

    def gerar_exercicio(self):
        if self.dificuldade == 1:
            palavra = random.choice(["casa", "bola", "janela"])
            return (f"Escreva corretamente a palavra '{palavra}'", palavra)

        elif self.dificuldade == 2:
            return ("Qual é o sujeito da frase: 'O menino correu'?", "o menino")

        else:
            return ("Classifique a palavra 'feliz'", "adjetivo")

    def corrigir(self, exercicio, resposta):
        return resposta.strip().lower() == exercicio[1].lower()


@app.route("/gerar", methods=["POST"])
def gerar():
    dados = request.json
    materia = dados.get("materia")
    dificuldade = dados.get("dificuldade")

    if materia == "matematica":
        d = Matematica()
    else:
        d = Portugues()

    if dificuldade == "facil":
        d.dificuldade = 1
    elif dificuldade == "medio":
        d.dificuldade = 2
    else:
        d.dificuldade = 3

    perg, resp = d.gerar_exercicio()

    return jsonify({
        "pergunta": perg,
        "resposta": resp
    })


@app.route("/")
def home():
    return "Servidor funcionando!"

if __name__ == "__main__":
    app.run(debug=True)
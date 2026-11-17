"""Gera o site "Professores em Ação" a partir de Python.

Uso:  python build.py
Saída: pasta site/ (é ela que o GitHub Pages publica).
"""
import shutil
from html import escape
from pathlib import Path

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "site"

# Menu "Conteúdos": (texto, arquivo). None = link "#"
MENU = [
    ("Introdução", "painel.html"),
    ("Variáveis", "variaveis.html"),
    ("Algoritmos", "algoritmos.html"),
    ("Strings", None),
    ("Iteração", None),
    ("Função", None),
]

EXERCICIOS = ["Exercício 1", "Exercício 2", "Exercício 3"]

# Cada página: arquivo -> (título, parágrafos em HTML)
PAGINAS = {
    "variaveis.html": (
        "Variáveis",
        [
            "Uma variável guarda um valor com um nome, por exemplo <code>nota = 8.5</code>.",
            "Depois, você usa o nome em vez de repetir o valor. "
            "Se a nota mudar, basta alterar em um só lugar.",
            'Exemplo: <code>aluno = "Ana"</code> e <code>faltas = 3</code>.',
        ],
    ),
    "algoritmos.html": (
        "Algoritmos",
        [
            "Um algoritmo é uma sequência de passos para resolver um problema.",
            "Exemplo: para calcular a média, some as notas e divida pela quantidade.",
        ],
    ),
}

# No site estático não há servidor, então o aviso das áreas continua no navegador.
SCRIPT_AREAS = """<script>
    try {
      var areas = JSON.parse(sessionStorage.getItem("areas") || "[]");
      if (areas.length) {
        var p = document.getElementById("areas-escolhidas");
        p.textContent = "Exemplos adaptados para: " + areas.join(", ") + ".";
        p.hidden = false;
      }
    } catch (e) {}
  </script>"""


def menu_html(arquivo_atual):
    itens = []
    for nome, destino in MENU:
        href = destino or "#"
        atual = ' aria-current="page"' if destino == arquivo_atual else ""
        itens.append(f'          <li><a class="menu__item" href="{href}"{atual}>{escape(nome)}</a></li>')
    return "\n".join(itens)


def exercicios_html():
    return "\n".join(f'          <li><a href="#">{escape(e)}</a></li>' for e in EXERCICIOS)


def pagina_html(arquivo, titulo, paragrafos):
    texto = "\n".join(f"          <p>{p}</p>" for p in paragrafos)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)} · Professores em Ação</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="app">

    <header class="topo">
      <h1 class="topo__titulo">Professores em Ação</h1>
      <nav class="topo__acoes" aria-label="Conta">
        <a href="index.html">Sair</a>
        <a href="#">Perfil</a>
      </nav>
    </header>

    <div class="corpo">

      <nav class="menu" aria-label="Conteúdos">
        <h2 class="menu__titulo">Conteúdos</h2>
        <ul class="menu__lista">
{menu_html(arquivo)}
        </ul>
      </nav>

      <main class="conteudo">
        <h2 class="conteudo__titulo">{escape(titulo)}</h2>
        <div class="conteudo__texto">
          <p id="areas-escolhidas" hidden></p>
{texto}
        </div>
      </main>

      <aside class="exercicios" aria-label="Exercícios">
        <h2 class="exercicios__titulo">Exercícios</h2>
        <ul class="exercicios__lista">
{exercicios_html()}
        </ul>
      </aside>

    </div>
  </div>

  {SCRIPT_AREAS}
</body>
</html>
"""


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir()

    # Páginas geradas por Python
    for arquivo, (titulo, paragrafos) in PAGINAS.items():
        (SAIDA / arquivo).write_text(pagina_html(arquivo, titulo, paragrafos), encoding="utf-8")

    # Arquivos que continuam como estão (login, painel, estilos)
    for nome in ["index.html", "painel.html", "style.css", "login.css"]:
        origem = RAIZ / nome
        if origem.exists():
            shutil.copy(origem, SAIDA / nome)

    print("Site gerado em", SAIDA)


if __name__ == "__main__":
    main()


# 🐦 Flappy Bird - Python

Um clone simples do clássico Flappy Bird desenvolvido em Python com Pygame.  
Você pode simplesmente **jogar** através do arquivo executável, ou acessar o **código-fonte** para estudar, modificar e melhorar.

---

## 🎮 Orientações para Quem Quer Jogar (Usuário Final)

### ✅ Passo a passo:

1. Acesse a pasta **`dist`** (ela foi gerada automaticamente quando o executável foi criado).
2. Dentro da pasta, você encontrará:
   - `Flappy_Bird.exe` (ou `main.exe`, dependendo do nome que você usou na hora de gerar).
   - Pasta **`imgs`** → Contém as imagens do jogo.
   - Pasta **`sounds`** → Contém os sons do jogo.
   - Arquivo **`recorde.txt`** → Onde sua maior pontuação fica salva.

### 🚩 Como Jogar:

- Dê dois cliques no arquivo `Flappy_Bird.exe`.
- O jogo abrirá em uma janela própria.
- **Use a tecla ESPAÇO para fazer o pássaro pular.**
- Quando perder, pressione:
  - **ESPAÇO** → Para reiniciar.
  - **ESC** → Para sair.

### ⚠️ Atenção:

- Não remova nem mova as pastas **`imgs`**, **`sounds`** e o arquivo **`recorde.txt`**.
- Eles precisam estar **na mesma pasta** do executável para que o jogo funcione corretamente.

---

## 🛠️ Orientações para Quem Quer Modificar o Código (Programador)

### 🐍 Requisitos:

- Ter o **Python** instalado (versão 3.8 ou superior):  
👉 https://www.python.org/downloads/

- Instalar a biblioteca **Pygame**:

```bash
pip install pygame
```

### 📂 Estrutura do Projeto:

```
Flappy_Bird-Python
│
├── imgs         → Imagens do jogo (cano, fundo, chão, pássaro)
├── sounds       → Sons do jogo (jump, hit, point)
├── recorde.txt  → Arquivo que salva sua maior pontuação
├── main.py      → Código principal do jogo
└── README.md    → Este manual
```

### ▶️ Como Rodar o Código:

1. Abra o terminal (Prompt de comando, Powershell ou terminal do VS Code).
2. Navegue até a pasta onde está o `main.py`.
3. Execute:

```bash
python main.py
```

O jogo será iniciado.

---

## 🚀 Como Gerar o Executável (Opcional)

Se quiser gerar seu próprio executável:

### Instale o PyInstaller:

```bash
pip install pyinstaller
```

### Gere o executável **sem abrir o CMD junto**:

```bash
pyinstaller --noconsole --onefile main.py
```

- O executável estará na pasta `dist`.
- Copie também as pastas **`imgs`**, **`sounds`** e o arquivo **`recorde.txt`** para essa pasta.

---

## 📜 Licença

Projeto livre para **estudo, aprendizado e modificações pessoais**.  
Proibido uso comercial sem autorização.

---

Desfrute e divirta-se! 🎉🐤

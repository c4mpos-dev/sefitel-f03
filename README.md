# ⚡ Simulador Interativo: Lei de Gauss (Casca Esférica)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

> Uma aplicação web interativa desenvolvida para o Seminário de Física III, demonstrando o comportamento do Campo Elétrico e Potencial em uma casca esférica condutora.

---

## 📸 Demonstração

🔗 **Acesse Online:** [sefitel-f03-grupo21](https://sefitel-f03-grupo21.streamlit.app/)

---

## 🚀 Funcionalidades

Este projeto utiliza **Python** e renderização via GPU (**Plotly**) para calcular e visualizar fenômenos eletrostáticos em tempo real.

* **🎛️ Controles Interativos:** Ajuste o **Raio ($R$)** da casca e a **Carga Total ($Q$)** instantaneamente.
* **🌡️ Mapa de Calor (2D):** Visualização da intensidade do Campo Elétrico ($|E|$).
* **↗️ Vetores de Campo:** Linhas de campo vetoriais que reagem à polaridade da carga.
* **🏔️ Topologia 3D:** Visualização do Potencial Elétrico ($V$) como uma superfície, demonstrando o platô de potencial constante no interior da esfera.
* **🎨 UI "Sci-Fi":** Interface escura estilizada com CSS personalizado para apresentações.

---

## 📚 Fundamentação Teórica

A simulação baseia-se na aplicação da **Lei de Gauss** para uma geometria esférica com distribuição superficial de carga.

### 1. Campo Elétrico ($E$)
$$\oint \vec{E} \cdot d\vec{A} = \frac{Q_{int}}{\epsilon_0}$$

* **Região Interna ($r < R$):** Como não há carga encapsulada pela superfície gaussiana ($Q_{int} = 0$), o campo é nulo.
    $$E = 0$$
    *(Blindagem Eletrostática)*

* **Região Externa ($r \ge R$):** A casca comporta-se como uma carga pontual concentrada no centro.
    $$E = \frac{1}{4\pi\epsilon_0} \cdot \frac{Q}{r^2}$$

### 2. Potencial Elétrico ($V$)
O potencial é contínuo em todo o espaço. No interior, ele assume o mesmo valor da superfície (gradiente nulo).

---

## 🛠️ Instalação e Execução Local

Para rodar este projeto na sua máquina:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/c4mpos-dev/sefitel-f03.git](https://github.com/c4mpos-dev/sefitel-f03.git)
    cd seu-repositorio
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app-seminario.py
    ```

---

## 📦 Estrutura do Projeto

* `app_seminario.py`: Código principal contendo a lógica física (NumPy), interface (Streamlit) e gráficos (Plotly).
* `requirements.txt`: Lista de bibliotecas necessárias para deploy na nuvem.
* `README.md`: Documentação do projeto.

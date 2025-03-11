import os
import fitz  # PyMuPDF para manipular PDFs
import streamlit as st
from pyngrok import ngrok

# Definir a pasta onde estão os arquivos PDF
PASTA_DE_TRABALHO = r"C:\Users\Bruna\PycharmProjects\PythonProject\arquivos"


def listar_pdfs(pasta):
    """Retorna uma lista de caminhos completos dos arquivos PDF na pasta especificada."""
    return [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".pdf")]


def extrair_texto_pdf(caminho_pdf):
    """Extrai o texto de um arquivo PDF."""
    try:
        doc = fitz.open(caminho_pdf)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text("text") + "\n"  # Captura o texto de cada página
        return texto
    except Exception as e:
        return f"Erro ao ler {caminho_pdf}: {e}"


def carregar_base_de_dados():
    """Carrega todos os PDFs da pasta e armazena o texto extraído em um dicionário."""
    base_de_dados = {}
    arquivos_pdf = listar_pdfs(PASTA_DE_TRABALHO)

    for arquivo in arquivos_pdf:
        nome_arquivo = os.path.basename(arquivo)  # Nome do arquivo sem o caminho
        base_de_dados[nome_arquivo] = extrair_texto_pdf(arquivo)

    return base_de_dados


def buscar_resposta(pergunta, base_de_dados):
    """Procura a pergunta nos textos armazenados e retorna trechos relevantes."""
    resposta = []
    for nome_arquivo, texto in base_de_dados.items():
        if pergunta.lower() in texto.lower():
            resposta.append(f"📄 **{nome_arquivo}**: {texto[:500]}...\n")  # Exibe os primeiros 500 caracteres
    return resposta if resposta else ["Nenhuma informação encontrada nos arquivos."]


# Configuração do Streamlit
st.title("📚 Framework de Pesquisa em PDFs")
st.write("Faça perguntas sobre os arquivos armazenados na pasta.")

# Carregar base de dados
base_de_dados = carregar_base_de_dados()
st.sidebar.write(f"📂 **{len(base_de_dados)} arquivos carregados**")

# Input da pergunta
pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    resultados = buscar_resposta(pergunta, base_de_dados)
    for r in resultados:
        st.write(r)

# Configurar o ngrok para gerar URL pública
public_url = ngrok.connect(8501).public_url
st.sidebar.write(f"🔗 **Acesse externamente:** [Clique aqui]({public_url})")

st.sidebar.success(f"Aplicação rodando em: {public_url}")

#Rodar no Terminal:  pip install streamlit pyngrok pymupdf
#streamlit run "Projeto Hanto.py"
#Até o momento ele permite fazer perguntas mas não elabora as respostas
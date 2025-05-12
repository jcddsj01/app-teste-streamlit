import streamlit as st
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os

# Tentar carregar variáveis do .env local (apenas em ambiente local)
load_dotenv()

# Função para pegar variável de ambiente ou dos secrets
def get_env(key):
    return (
        os.getenv(key) or
        st.secrets["general"].get(key)
    )

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host=get_env("DB_HOST"),
        port=int(get_env("DB_PORT")),
        user=get_env("DB_USER"),
        password=get_env("DB_PASSWORD"),
        database=get_env("DB_NAME")
    )

# Criar tabela caso não exista
def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            idade INT,
            profissao VARCHAR(100),
            salario DECIMAL(10,2),
            data_hora DATETIME
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Inserir dados
def inserir_dados(nome, idade, profissao, salario):
    conn = conectar_banco()
    cursor = conn.cursor()
    data_hora = datetime.now()
    cursor.execute("""
        INSERT INTO pessoas (nome, idade, profissao, salario, data_hora)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, idade, profissao, salario, data_hora))
    conn.commit()
    cursor.close()
    conn.close()

# Listar dados
def listar_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, idade, profissao, salario, data_hora FROM pessoas ORDER BY id DESC")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

# =====================
# 🖥️ Interface Streamlit
# =====================

st.title("Cadastro de Pessoas")

with st.form("formulario"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    profissao = st.text_input("Profissão")
    salario = st.number_input("Salário", min_value=0.0, step=0.01)
    enviado = st.form_submit_button("Enviar")

if enviado:
    if nome and profissao:
        criar_tabela()
        inserir_dados(nome, idade, profissao, salario)
        st.success("✅ Dados salvos com sucesso!")
    else:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")

# Exibir dados
st.subheader("📋 Registros salvos")
for linha in listar_dados():
    st.write(f"🧑 {linha[0]}, {linha[1]} anos, {linha[2]}, R$ {linha[3]:.2f} — {linha[4].strftime('%d/%m/%Y %H:%M:%S')}")

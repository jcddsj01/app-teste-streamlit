import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis do .env
load_dotenv()

# Função para conectar ao banco
def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Função para criar tabela (executada uma vez)
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

# Função para inserir dados
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

# Interface do Streamlit
st.title("Cadastro de Pessoas")

with st.form("formulario"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    profissao = st.text_input("Profissão")
    salario = st.number_input("Salário", min_value=0.0, step=0.01)
    enviado = st.form_submit_button("Enviar")

if enviado:
    if nome and profissao:
        criar_tabela()  # cria a tabela se não existir
        inserir_dados(nome, idade, profissao, salario)
        st.success("Dados salvos com sucesso!")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios.")

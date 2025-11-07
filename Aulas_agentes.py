import os 
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

#AGENTES PARA ESTUDO
st.header("Agentes para Estudo")
st.write("Informe o tema e gere material didático para estudar")

tema = st.text_input("Tema de estudo: ", placeholder="Ex.:Algoritmos")
objetivo = st.text_input("Objetivo: ",placeholder="Ex.:Entender conceitos")

executar = st.button("Gerar material")
api_key = 'SUA_CHAVE_API'

if executar:
    #características
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3 
        #temperature: define o nível de criatividade
        #<= 0.3 mais determinístico
        #entre 0.4 e 0.7 equilibrado para explicação
        #maior que 0.7 mais criativo
    )

#Agentes
agente_resumo = agent(
    role="Redator de resumo didático",
    # O que deve fazer. 
    goal=(
        "Escrever RESUMO claro e didático sobre {tema} alinhado com o {objetivo}."
        "A linguagem deve ser didática, direta com contexto prático e sem jargões"
    ),
    backstory= "Você transforma temas técnicos/acadêmicos em explicações curtas e precisas.",
    llm= llm, verbose=False
)

agente_exemplos = agent(
    role="Criador de exemplos contextualizados",
    goal=(
        "Gerar 5 EXEMPLOS CURTOS sobre {tema}, cada um com contexto realista."
        "Cada exemplo com título (em negrito), cenário, dados(se houver), aplicação e resultado"
    ),
    backstory= "Você mostra o conceito em ação com exemplos breves e concretos.",
    llm=llm, verbose=false
)

agente_exercicios = agent(
    role="Criador de exercícios",
    goal=(
        "Criar 4 EXERCÍCIOS SIMPLES sobre {tema}"
        "Variar formato (múltipla escolha, V/F, completar, resolução curta)."
        "Enunciados claros. NÃO incluir respostas"
    ),
    backstory= "Você cria atividades rápidas qie fixam conceitos essenciais",
    llm=llm, verbose=false
)
agente_gabarito = agent(
    role="Revisor e gabaritador",
    goal=(
        "Ler os EXERCÍCIOS sobre {tema} e produzir GABARITO oficial, com respostas corretas e justificativa breve (1-3 frases) por item"
    ),
    backstory= "Você confere consistência e explica rapidamente o porquê da resposta.",
    llm=llm, verbose=false

import os 
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

#AGENTES PARA ESTUDO
st.header("Agentes para Estudo")
st.write("Informe o tema e gere material didático para estudar")

tema = st.text_input("Tema de estudo: ", placeholder="Ex.:Algoritmos")
objetivo = st.text_input("Objetivo: ",placeholder="Ex.:Entender conceitos")

executar = st.button("Gerar material")
api_key = 'SUA CHAVE API'

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

t_resumo = task(
    description=(
        "RESUMO: escreva em português do Brasil um resumo didático sobre {tema} e objetivo {objetivo}"
        "inclua: definição (3-4 frases), por que importa (2-3), onde se aplica (2,3) e 4-6 ideias chaves"
        "com marcadores.Formate em Markdown com título."
    ),
    agent=agente_resumo,
    expected_output= "Resumo em Markdown com título, parágrafos curtos e 4-6 marcadores(bullets)"
)

t_exemplos = task(
    description=(
        "Padrão (até 5 linhas cada): Título, cenário, dados/entrada, como aplicar (1-2 frases), resultado"
    ),
    agent=agente_exemplos,
    expected_output = "Lista numerada(1-4) em Markdown com exemplos curtos e completos"

)

t_exercicios=task(
    description=(
        "EXERCÍCIOS:crie 4 exercícios simples sobre {tema} em PT-BR"
        "Varie formatos e não inclua respostas"
        "Entregue lista numerada(1-4) em Markdown"
    ),
    agent=agente_exercicios,
    expected_output="Lista numerada (1-4) com exercícios simples, sem respostas"
)

t_gabarito=task(
    description=(
        "GABARITO: Com base nos EXERCÍCIOS fornecidos no contexto, produza as respostas corretas"
        "Para cada item, dê:\n"
        "- Resposta: (letra, valor, solução)\n"
        "- Comentário: justificativa breve e direta (1-2 frases), citando o ceonceito-chave\n"
        "Formato: Lista numerada (1 a 3) em Markdown."
    ),
    agent=agente_gabarito,
    expected_output="Lista numerada (1 a 3) com resposta e comentário por exercício.",
    context=[t_exercicios]

)
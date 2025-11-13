import os 
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

#Agentes para criação de cenários:
st.header("Criador de cenários")
st.write("informe os parâmetros")

tematica = st.text_input("Digite a temática(obrigatório)" , placeholder="Ex:Cidade no Inverno")
caracteristicas = st.text_input("Digite as características indispensaveis", placeholder="EX: Grande e tecnológica")
economia = st.text_input("Digite no que se baseia a economia local", placeholder= "Ex:turismo")
pessoas = st.text_input("Digite caracteristicas da população local", placeholder= "EX:desabitado")
governo = st.text_input("Digite o sistema de governo", placeholder="EX:Democracia")

executar = st.button("Gerar material")
api_key = 'SUA CHAVE API'

if executar:
    #características
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.9 
        #temperature: define o nível de criatividade
        #<= 0.3 mais determinístico
        #entre 0.4 e 0.7 equilibrado para explicação
        #maior que 0.7 mais criativo
    )

    #agentes
    agente_historia = Agent(
        role="Contador de histórias",
        goal=(
            "Inventar a HISTÓRIA do passado do local."
            "A HISTÓRIA do local deve estar de acordo com a {tematica} e com as {caracteristicas}"
            "A HISTÓRIA também deve justificar e explicar o {governo} e a {economia} "
        ),
        backstory= "Você usa características para inventar histórias de lugares fictícios para um jogo.",
        llm= llm, verbose= False
    )

    agente_descricao = Agent(
        role= "Descritor de cenários",
        goal=(
            "Ler a HISTÓRIA do local e criar uma DESCRIÇÃO do lugar a partir dela."
            "A DESCRIÇÃO deve ser detalhista e estar de acordo com as {caracteristicas}."
            "Primeiro descreve-se a aparência do lugar e depois as atividades economicas e de entretenimento. Use o {governo} e a {economia} como referência."
        ),
        backstory= "Você descreve os locais criados para os jogadores do jogo.",
        llm=llm, verbose= False
    )

    agente_populacao = Agent(
        role= "Criador de identidades",
        goal=(
            "Ler a HISTÓRIA e a DESCRIÇÃO do lugar e inventar os tipos de pessoas que vivem no local de acordo com as características de {pessoas}."
            "Primeiro deve-se dar descrições gerais dos tipos de pessoas que estão presentes."
            "Depois deve se apresentar uma lista com até 20 pessoas importantes. Para essas pessoas, invente nomes, ocupação e um breve histórico"
        ),
        backstory="Você cria e fala das pessoas que viveriam no local criado para o jogo",
        llm=llm, verbose=False
    )

    #tarefas
    t_historia = Task(
        description=(
            "HISTÓRIA: escreva em português do Brasil a história de um lugar fictício. Invente também um nome para o local."
            "A HISTÓRIA deve ser inventada e estar de acordo com a {tematica} e com as {caracteristicas}."
            "inclua uma explicação do {governo} e da {economia}. Formate em Markdown com título."

        ),
        agent=agente_historia,
        expected_output= "Um texto em Markdown com título, parágrafos curtos e linguagem detalhada."
    )

    t_descricao = Task(
        description=(
            "DESCRIÇÃO: escreva uma descrição do local da HISTÓRIA atualmente."
            "Escreva em formato narrativo e inclua as informações de {tematica}, {governo} e {economia}."
        ),
        agent=agente_descricao,
        expected_output= "Um texto narrativo em Markdown com parágrafos curtos.",
        context=[t_historia]
    )

    t_populacao=Task(
        description=(
            "leia a DESCRIÇÃO, invente e descreva as pessoas que habitam o local."
            "Comece com uma descrição dos tipos de pessoas que estão no local. Utilize as características de {pessoas}."
            "Depois invente e escreva uma lista com 20 pessoas que seriam importantes. Crie nome, ocupação e uma breve descrição(5-10 linhas) das pessoas na lista."
            "Escreva a lista com uma entrada para cada pessoa, em Markdown, com tópicos na ordem: nome,ocupação, descrição."
        ),
        agent=agente_populacao,
        expected_output="Lista em que cada entrada tem 3 tópicos, em markdown e em português do Brasil",
        context=[t_descricao]
    )

    #Equipe
    agents= [agente_historia,agente_descricao,agente_populacao]
    tasks= [t_historia,t_descricao,t_populacao]
    crew = Crew(
        agents=agents,
        tasks=tasks,
        Process=Process.sequential
        )
        
    crew.kickoff(inputs={
        "tematica":tematica,
        "caracteristicas":caracteristicas or "não informado",
        "economia":economia or "não informado",            
        "pessoas":pessoas or "não informado",
        "governo":governo or "não informado",

        })

        #exibir resultados.
    historia_out= getattr(t_historia,"output",None) or getattr(t_historia,"result","") or ""
    descricao_out= getattr(t_descricao,"output",None) or getattr(t_descricao,"result","") or ""
    populacao_out= getattr(t_populacao,"output",None) or getattr(t_populacao,"result","") or ""

        #Aba para mostrar resultados
    aba_historia, aba_descricao, aba_populacao = st.tabs(
        ["História","Descrição","População"]
        )

    with aba_historia:
        st.markdown(historia_out)
    with aba_descricao:
        st.markdown(descricao_out)
    with aba_populacao:
        st.markdown(populacao_out) 
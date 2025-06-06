import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langserve import add_routes
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Cargar variables de entorno desde un archivo .env para desarrollo local
load_dotenv()

# --- 1. Carga de Datos y Creación del VectorStore ---
promtior_content = """
About Promtior
In November 2022, ChatGPT was released, causing a significant impact.
In May 2023, Promtior was founded facing this context. The key
question is: how to approach a scenario of transversal disruption and
maximize the opportunities it presents?
Through its technological and organizational consulting, Promtior offers
a way to generate new business models, answering this question and
bringing companies at the forefront of their sector.
Promtior offers services like technological and organizational consulting.
"""

# Genero los fragmentos (chunks)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.create_documents([promtior_content])

# Creo embeddings y el VectorStore (usando el modelo de embeddings de OpenAI)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# Crear el retriever desde el VectorStore
retriever = vectorstore.as_retriever()

# --- 2. Creación de la Cadena RAG ---

# Plantilla del Prompt
template = """
Eres un asistente que responde preguntas sobre la empresa Promtior.
Usa únicamente el siguiente contexto recuperado para responder la pregunta.
Si no sabes la respuesta basándote en el contexto, di "No tengo suficiente información para responder a esa pregunta".
Sé conciso y responde en un máximo de tres frases.

Pregunta: {question}
Contexto: {context}
Respuesta:
"""
prompt = ChatPromptTemplate.from_template(template)

# Modelo de Lenguaje (LLM)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Creación de la cadena RAG completa
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 3. Configuración de la App con FastAPI y LangServe ---

app = FastAPI(
    title="Promtior RAG Chatbot",
    version="1.0",
    description="Una API para un chatbot sobre Promtior usando RAG",
)

# Añadir la ruta para interactuar con la cadena RAG
add_routes(
    app,
    rag_chain,
    path="/promtior-assistant",
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

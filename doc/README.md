Resumen del Proyecto:

El desafío consistió en desarrollar y desplegar un chatbot conversacional utilizando la arquitectura RAG (Retrieval Augmented Generation) para responder preguntas sobre la empresa Promtior. El objetivo era utilizar el contenido del sitio web de la empresa como base de conocimiento.

Mi enfoque para resolver el desafío se basó en los siguientes pasos:

Extracción de Datos: 
El primer paso, y uno de los más importantes, es la recopilación de datos. Para este proyecto, se extraería manualmente el texto relevante del sitio web de Promtior y de la presentación proporcionada para asegurar una base de conocimiento limpia y precisa.

Arquitectura RAG con LangChain: 
Implementé la solución en Python utilizando la biblioteca LangChain. La lógica principal consiste en tomar el texto extraído, dividirlo en fragmentos (chunks), y generar embeddings (representaciones vectoriales) para cada fragmento usando los modelos de OpenAI. Estos vectores se almacenan en un VectorStore en memoria (FAISS) para una búsqueda rápida de similitud.

Flujo de Consulta: 
Cuando un usuario hace una pregunta, el sistema primero busca en el VectorStore los fragmentos de texto más relevantes para la pregunta. Luego, estos fragmentos (el "contexto recuperado") se inyectan en un prompt junto con la pregunta original. Finalmente, el modelo de lenguaje (LLM), en este caso gpt-3.5-turbo de OpenAI, genera una respuesta basada tanto en la pregunta como en el contexto proporcionado.

API con LangServe: 
Para exponer la lógica del chatbot como un servicio, utilicé LangServe, que permite desplegar cualquier cadena de LangChain como una API RESTful de manera sencilla.
Despliegue: La solución fue diseñada para ser desplegada fácilmente en la nube. Se eligió Railway por su simplicidad para desplegar aplicaciones Python, configurando las variables de entorno necesarias (como la API key de OpenAI) y los archivos de configuración (Procfile, requirements.txt).

Flujo de los componentes:
Usuario: 
Inicia el proceso haciendo una pregunta a través de una interfaz de cliente (ej. una llamada a la API).

API Endpoint (LangServe en Railway): 
Recibe la solicitud HTTP del usuario.

Cadena RAG (LangChain): 
Orquesta el flujo principal.
  Paso 3a (Recuperación): La pregunta del usuario se envía al componente Retriever.
  Retriever (desde FAISS VectorStore): El Retriever busca en el VectorStore FAISS los documentos de texto más relevantes para la pregunta. Este VectorStore fue previamente poblado con los embeddings del contenido de Promtior.
  Paso 3b (Aumento): Los documentos recuperados (el contexto) y la pregunta original se combinan en una plantilla de Prompt.
  Paso 3c (Generación): El Prompt completo se envía al Modelo de Lenguaje (LLM - OpenAI).
  
LLM (OpenAI API): 
Genera una respuesta coherente basada en la información del Prompt.


# Documentación del Proyecto: Chatbot Asistente para Promtior

## Resumen del Proyecto

El desafío consistió en desarrollar y desplegar un chatbot conversacional utilizando la arquitectura **RAG (Retrieval Augmented Generation)** para responder preguntas sobre la empresa Promtior, basándose en el contenido de su sitio web y documentación de apoyo.

Mi enfoque para resolver el desafío se basó en los siguientes pasos:
1.  **Extracción de Datos**: Se extrajo el texto relevante del sitio web de Promtior y de la presentación proporcionada para asegurar una base de conocimiento limpia y precisa.
2.  **Arquitectura RAG con LangChain**: Se implementó la solución en Python utilizando la biblioteca **LangChain**. La lógica consiste en tomar el texto extraído, dividirlo en fragmentos (`chunks`), y generar *embeddings* vectoriales para cada fragmento usando OpenAI. Estos vectores se almacenan en un `VectorStore` en memoria (FAISS) para una búsqueda rápida de similitud.
3.  **Flujo de Consulta**: Cuando un usuario hace una pregunta, el sistema primero busca en el `VectorStore` los fragmentos de texto más relevantes. Estos fragmentos (el "contexto") se inyectan en un *prompt* junto con la pregunta original. Finalmente, el modelo de lenguaje (LLM) de OpenAI genera una respuesta basada únicamente en el contexto proporcionado.
4.  **API con LangServe**: Para exponer la lógica como un servicio, se utilizó **LangServe**, que permite desplegar cualquier cadena de LangChain como una API RESTful de manera sencilla.
5.  **Despliegue**: La solución fue desplegada en **Railway**, una plataforma en la nube que simplifica enormemente el proceso al integrarse directamente con GitHub y gestionar la configuración a través de archivos como el `Procfile` y las variables de entorno.

El principal desafío fue asegurar que el contexto recuperado fuera lo suficientemente preciso para responder a las preguntas sin "alucinar" o inventar información. Esto se mitigó con un *prompt* claro que instruye al modelo a basar su respuesta estrictamente en la información proporcionada.

## Diagrama de Componentes

Este diagrama ilustra el flujo de la solución, desde la pregunta del usuario hasta la respuesta final.

1.  **Usuario**: Inicia el proceso haciendo una pregunta a través de una llamada a la API.
2.  **API Endpoint (LangServe en Railway)**: Recibe la solicitud del usuario.
3.  **Cadena RAG (LangChain)**: Orquesta el flujo principal.
    * **Paso 3a (Recuperación)**: La pregunta se envía al componente **Retriever**.
    * **Retriever (desde FAISS VectorStore)**: Busca en el **VectorStore FAISS** los documentos de texto más relevantes para la pregunta.
    * **Paso 3b (Aumento)**: Los documentos recuperados (el contexto) y la pregunta original se combinan en una plantilla de **Prompt**.
    * **Paso 3c (Generación)**: El **Prompt** completo se envía al **Modelo de Lenguaje (LLM - OpenAI)**.
4.  **LLM (OpenAI API)**: Genera una respuesta coherente basada en la información del Prompt.
5.  **Respuesta**: La respuesta generada por el LLM se devuelve a través de la API al usuario.

Respuesta:
La respuesta generada por el LLM se devuelve a través de LangServe al usuario.

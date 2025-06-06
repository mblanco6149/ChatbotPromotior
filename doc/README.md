Resumen del Proyecto
El desafío consistió en desarrollar y desplegar un chatbot conversacional utilizando la arquitectura RAG (Retrieval Augmented Generation) para responder preguntas sobre la empresa Promtior. El objetivo era utilizar el contenido del sitio web de la empresa como base de conocimiento.

Mi enfoque para resolver el desafío se basó en los siguientes pasos:

Extracción de Datos: El primer paso, y uno de los más importantes, es la recopilación de datos. Para este proyecto, se extraería manualmente el texto relevante del sitio web de Promtior y de la presentación proporcionada para asegurar una base de conocimiento limpia y precisa.
Arquitectura RAG con LangChain: Implementé la solución en Python utilizando la biblioteca LangChain. La lógica principal consiste en tomar el texto extraído, dividirlo en fragmentos (chunks), y generar embeddings (representaciones vectoriales) para cada fragmento usando los modelos de OpenAI. Estos vectores se almacenan en un VectorStore en memoria (FAISS) para una búsqueda rápida de similitud.
Flujo de Consulta: Cuando un usuario hace una pregunta, el sistema primero busca en el VectorStore los fragmentos de texto más relevantes para la pregunta. Luego, estos fragmentos (el "contexto recuperado") se inyectan en un prompt junto con la pregunta original. Finalmente, el modelo de lenguaje (LLM), en este caso gpt-3.5-turbo de OpenAI, genera una respuesta basada tanto en la pregunta como en el contexto proporcionado.
API con LangServe: Para exponer la lógica del chatbot como un servicio, utilicé LangServe, que permite desplegar cualquier cadena de LangChain como una API RESTful de manera sencilla.
Despliegue: La solución fue diseñada para ser desplegada fácilmente en la nube. Se eligió Railway por su simplicidad para desplegar aplicaciones Python, configurando las variables de entorno necesarias (como la API key de OpenAI) y los archivos de configuración (Procfile, requirements.txt).
El principal desafío fue asegurar que el contexto recuperado fuera lo suficientemente preciso para responder a las preguntas sin alucinar. Esto se mitigó ajustando el proceso de división de texto y asegurando que el prompt instruyera claramente al modelo para basar su respuesta únicamente en el contexto proporcionado.

Flujo de los componentes:
Usuario: Inicia el proceso haciendo una pregunta a través de una interfaz de cliente (ej. una llamada a la API).
API Endpoint (LangServe en Railway): Recibe la solicitud HTTP del usuario.
Cadena RAG (LangChain): Orquesta el flujo principal.
  Paso 3a (Recuperación): La pregunta del usuario se envía al componente Retriever.
  Retriever (desde FAISS VectorStore): El Retriever busca en el VectorStore FAISS los documentos de texto más relevantes para la pregunta. Este VectorStore fue previamente poblado con los embeddings del contenido de Promtior.
  Paso 3b (Aumento): Los documentos recuperados (el contexto) y la pregunta original se combinan en una plantilla de Prompt.
  Paso 3c (Generación): El Prompt completo se envía al Modelo de Lenguaje (LLM - OpenAI).
LLM (OpenAI API): Genera una respuesta coherente basada en la información del Prompt.
Respuesta: La respuesta generada por el LLM se devuelve a través de LangServe al usuario.

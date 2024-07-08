import streamlit as st

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models





prompt_requerimiento = "Como experto en desarrollo de software analiza la imagen del siguiente diagrama para identificar los requerimientos funcionales de un proyecto especifico. Identifica el nombre y el identificador del proyecto (ID de proyecto) para futuras referencias. Genera la lista de casos de uso identificados. Incluye una redacción de las acciones de los actores. Analiza las clases y componentes para describir las especificaciones técnicas. Responde en idioma español."

def generate_requerimiento(document):
  vertexai.init(project="eco-llm-app", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=[prompt_requerimiento]
   
  )
  responses = model.generate_content(
      ["""Diagrama de funcionalidad""", Part.from_data(
    mime_type="application/pdf",
    data=base64.b64decode(document))],
      generation_config=generation_config,
      safety_settings=safety_settings,
      stream=True,
  )


  requerimiento = ""
  for response in responses:
    requerimiento += response.text + '\n'
  return requerimiento




generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


# Show title and description.
st.title("📄 Ecoarchitecture Cognitive Agent Developer")
st.write(
    "Adjunta el diagrama del requerimiento para iniciar el proceso de desarrollo "
    "To use this app, you need to provide an Vertex Gemini Pro API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

model_api_key = st.text_input(" Gemini API Key", type="password")

if not model_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("pdf")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
       


        # Stream the response to the app using `st.write_stream`.
        st.write_stream(generate_requerimiento(document))









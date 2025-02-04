import streamlit as st
import utils

# Load environment variables
env_vars = utils.load_env_variables()
ai_endpoint = env_vars['ai_endpoint']
ai_key = env_vars['ai_key']
ai_project_name = env_vars['ai_project_name']
ai_deployment_name = env_vars['ai_deployment_name']

# Create client using endpoint and key
ai_client = utils.create_ai_client(ai_endpoint, ai_key)

st.write("""
# Chatbot Beamng
La idea de este chatbot es responder preguntas relacionadas con el juego Beamng Drive.
""")

# Chat interface
user_question = st.text_input("Pregunta:")
if user_question:
    answers = utils.get_answer_from_bot(ai_client, ai_project_name, ai_deployment_name, user_question)
    for candidate in answers:
        st.write(f"Respuesta: {candidate.answer}")
        st.write(f"Confianza: {candidate.confidence}")
        st.write(f"Fuente: {candidate.source}")

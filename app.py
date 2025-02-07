import streamlit as st
import utils

# Load environment variables
env_vars = utils.load_env_variables()
ai_endpoint = env_vars['ai_endpoint']
ai_key = env_vars['ai_key']
ai_project_name = env_vars['ai_project_name']
ai_deployment_name = env_vars['ai_deployment_name']

# Create AI client
ai_client = utils.create_ai_client(ai_endpoint, ai_key)

st.title("🤖 Chatbot BeamNG Drive")
st.write("Este chatbot responde preguntas sobre el juego BeamNG Drive.")

# Function to process user input
def process_input(user_question):
    st.markdown(f"**Usuario:** {user_question}")
    
    answers = utils.get_answer_from_bot(ai_client, ai_project_name, ai_deployment_name, user_question)
    if answers:
        bot_response = answers[0].answer
        follow_up_prompts = [prompt.display_text for prompt in answers[0].dialog.prompts] if hasattr(answers[0], 'dialog') and answers[0].dialog else []
    
    st.markdown(f"**Asistente:** {bot_response}")
    
    # Mostrar follow-up prompts
    if follow_up_prompts:
        selected_prompt = st.radio("¿Quieres preguntar algo más?", follow_up_prompts, index=None)
        if selected_prompt:
            process_input(selected_prompt)

# Procesar entrada del usuario
if user_question := st.text_input("Escribe tu pregunta..."):
    process_input(user_question)

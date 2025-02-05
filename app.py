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

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "follow_up_prompts" not in st.session_state:
    st.session_state["follow_up_prompts"] = []  # Lista de follow-ups
if "selected_follow_up" not in st.session_state:
    st.session_state["selected_follow_up"] = None  # Follow-up seleccionado

# Function to process user input
def process_input(user_question):
    st.session_state["messages"].append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)
    
    answers = utils.get_answer_from_bot(ai_client, ai_project_name, ai_deployment_name, user_question)
    if answers:
        bot_response = answers[0].answer
        follow_up_prompts = [prompt.display_text for prompt in answers[0].dialog.prompts] if hasattr(answers[0], 'dialog') and answers[0].dialog else []
    else:
        bot_response = "Lo siento, no tengo una respuesta para esa pregunta."
        follow_up_prompts = []
    
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Guardar los follow-up prompts en session state
    st.session_state["follow_up_prompts"] = follow_up_prompts

# Mostrar historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Procesar entrada del usuario
if user_question := st.chat_input("Escribe tu pregunta..."):
    process_input(user_question)

# Mostrar follow-up prompts como un selectbox si hay opciones disponibles
if st.session_state["follow_up_prompts"]:
    selected_prompt = st.selectbox("¿Quieres preguntar algo más?", [""] + st.session_state["follow_up_prompts"])

    # Si el usuario selecciona un follow-up prompt, procesarlo
    if selected_prompt and selected_prompt != st.session_state["selected_follow_up"]:
        st.session_state["selected_follow_up"] = selected_prompt  # Guardar selección
        process_input(selected_prompt)

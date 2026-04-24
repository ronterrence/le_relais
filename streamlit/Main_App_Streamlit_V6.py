# cd "DemoDay - Assistant Social"
# .\venv\Scripts\activate
# python -m streamlit run Main_App_Streamlit_V2.py
# npx n8n start

import streamlit as st
import requests

URL_N8N = "http://localhost:5678/webhook/DemoDay2"

st.set_page_config(page_title="Le Relais", page_icon="🤝")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1E40AF, #3B82F6) !important;
        }
        
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] .stMarkdown {
            color: white !important;
        }
        
        [data-testid="stSidebar"] input {
            color: #31333F !important;
        }
            
        [data-testid="stSidebar"] .stButton button {
            color: #1E40AF !important;
            background: white !important;
            border: 2px solid white !important;
            border-radius: 10px;
        }
            
        [data-testid="stSidebar"] .stButton > button p {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("Chatbot.png", width=250)
    st.divider()
    st.write("Renseigne ta localisation pour avoir des résultats personnalisés !")
    
    CP = st.text_input("📍 Ton code postal ici", placeholder="Ex : 69000")
    st.divider()
    st.info("*Grâce à ta localisation, je m'appuie sur les données officielles de l'État et sur ma base documentaire pour t'aider au mieux* 😉")
    st.divider()
    if st.button("🔄 *Réinitialiser notre discussion*", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

st.title("🤝 Le Relais")
st.divider()

st.markdown("""
### Bienvenue dans ton assistant social ! 👋
Je suis là pour t'aider à identifier des organismes locaux qui pourront t'aider selon les difficultés que tu rencontres, et te proposer des pistes d'aides qui te seront utiles. 

N'hésite pas à me poser toutes les questions que tu souhaites !
""")
st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not st.session_state["messages"]:
    st.markdown("**💡 Tu peux me demander par exemple :**")
    examples = [
        "🏠  J'ai des difficultés à payer mon loyer, quelles aides existent ?",
        "🍽️  Où puis-je trouver une aide alimentaire près de chez moi ?",
        "💼  J'ai besoin d'un emploi étudiant, quelles démarches dois-je faire ?",
    ]
    for ex in examples:
        st.markdown(f'<div class="example-card">{ex}</div>', unsafe_allow_html=True)
    st.divider()

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ton message...")

if user_input:
    if not CP:
        st.warning("⚠️ Entre ton code postal dans la barre latérale avant de discuter 🙂")
        st.stop()

    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Recherche en cours..."):
        try:
            res = requests.post(URL_N8N, json={"messages": st.session_state["messages"], "CP": CP})
            data = res.json()
            
            answer = data.get("response", data.get("output", "Réponse inattendue du serveur."))
        except Exception as e:
            answer = f"Erreur de connexion : {e}"

        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)


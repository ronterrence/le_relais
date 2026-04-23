# cd "DemoDay - Assistant Social"
# .\venv\Scripts\activate
# python -m streamlit run Main_App_Streamlit_V2.py
#npx n8n start

import streamlit as st
import requests
import re

URL_N8N = "http://localhost:5678/webhook/DemoDay2"

st.set_page_config(page_title="Assistant Social", page_icon="🤝")
st.title("🤝 Assistant Social – Chat")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

CP = st.text_input("Votre code postal", placeholder="Ex : 69000")

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Votre message...")

if user_input:

    if not CP:
        st.warning("Veuillez entrer votre code postal avant de discuter.")
        st.stop()

    if not re.fullmatch(r"\d{5}", CP):
        st.warning("Le code postal doit contenir exactement 5 chiffres.")
        st.stop()

    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Recherche en cours..."):
        try:
            res = requests.post(
                URL_N8N,
                json={
                    "messages": st.session_state["messages"],
                    "CP": CP
                }
            )

            try:
                data = res.json()
                answer = data.get("response", "Réponse inattendue du serveur.")
            except:
                answer = "Le serveur a renvoyé une réponse non valide."

            # Ajout du message assistant
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)

        except Exception:
            st.error("Erreur lors de l'appel au serveur.")


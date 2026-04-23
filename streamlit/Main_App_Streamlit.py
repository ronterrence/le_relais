# cd "DemoDay - Assistant Social"
# .\venv\Scripts\activate
# python -m streamlit run Main_App_Streamlit.py

import streamlit as st
import requests

URL_N8N = "https://abdellatif-issam.app.n8n.cloud/webhook/Demo-Day"

st.set_page_config(page_title="Assistant Social", page_icon="🤝", layout="centered")

st.title("🤝 Ton Assistant Social")
st.write("Trouvez des aides et des organismes pouvant vous accompagner près de chez vous.")

with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/fr/thumb/2/22/Republique-francaise-logo.svg/3840px-Republique-francaise-logo.svg.png",
        width=100
    )
    st.title("Ton Assistant Social")
    st.info("Cet assistant utilise les données officielles de l'État pour vous orienter.")
    st.divider()
    st.caption("Version 0.1")

with st.container(border=True):
    prompt = st.text_area("Comment peut-on vous aider ?", height=120)
    CP = st.text_input("Code Postal")

if st.button("Lancer la demande"):
    if not prompt or not CP:
        st.warning("Veuillez remplir tous les champs.")
    else:
        with st.spinner("Recherche en cours..."):
            try:
                # Timeout augmenté pour laisser n8n travailler
                res = requests.post(URL_N8N, json={"prompt": prompt, "CP": CP})

                data = res.json()
                reponse = data.get("response")

                if not reponse:
                    st.error("Aucune réponse trouvée.")
                else:
                    st.success("Terminé !")
                    st.chat_message("assistant").write(reponse)

            except Exception as e:
                st.error(f"Erreur : {e}")
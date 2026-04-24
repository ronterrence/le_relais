import os
import re

import requests
import streamlit as st


def get_setting(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        return os.getenv(name, default)


WEBHOOK_URL = get_setting("N8N_WEBHOOK_URL", get_setting("URL_N8N", ""))
N8N_URL = get_setting("N8N_WEBHOOK_URL", get_setting("URL_N8N"))



def setup_page() -> None:
    st.set_page_config(page_title="Assistant Social", page_icon="🤝", layout="centered")
    st.title("🤝 Assistant Social - Chat")
    st.caption("Version 4 - chat avec mémoire, reset, validation et meilleure gestion d'erreur.")


def init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("postal_code", "")



def validate_postal_code(postal_code: str) -> str:
    cp = postal_code.strip()
    if not cp:
        return "Veuillez entrer votre code postal avant de discuter."
    if not re.fullmatch(r"\d{5}", cp):
        return "Le code postal doit contenir exactement 5 chiffres."
    return ""



def clear_conversation() -> None:
    st.session_state["messages"] = []



def append_message(role: str, content: str) -> None:
    st.session_state["messages"].append({"role": role, "content": content})



def extract_answer(payload) -> str:
    if isinstance(payload, dict):
        return str(
            payload.get("response")
            or payload.get("answer")
            or payload.get("message")
            or "Réponse inattendue du serveur."
        )
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        first = payload[0]
        return str(
            first.get("response")
            or first.get("answer")
            or first.get("message")
            or "Réponse inattendue du serveur."
        )
    return "Le serveur a renvoyé une réponse non valide."



def call_n8n(messages: list[dict], postal_code: str) -> str:
    if not WEBHOOK_URL:
        return "Le webhook n8n n'est pas configuré. Ajoutez N8N_WEBHOOK_URL dans vos secrets ou variables d'environnement."

    response = requests.post(
        WEBHOOK_URL,
        json={"messages": messages, "CP": postal_code},
        timeout=60,
    )
    response.raise_for_status()
    return extract_answer(response.json())



def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("Configuration")
        st.info("Cette version conserve l'historique de conversation dans Streamlit.")

        st.session_state["postal_code"] = st.text_input(
            "Votre code postal",
            value=st.session_state["postal_code"],
            placeholder="Ex : 69000",
        ).strip()

        if st.button("Réinitialiser la conversation", use_container_width=True):
            clear_conversation()
            st.rerun()

        st.divider()
        st.caption("Variables reconnues")
        st.code("N8N_WEBHOOK_URL\nURL_N8N", language="text")
        st.caption("Le fichier .env local ou les secrets Streamlit sont recommandés.")



def render_history() -> None:
    if not st.session_state["messages"]:
        st.info("Commencez la discussion en écrivant un message et en ajoutant votre code postal.")
        return

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])



def handle_user_message(user_input: str) -> None:
    error = validate_postal_code(st.session_state["postal_code"])
    if error:
        st.warning(error)
        return

    append_message("user", user_input)
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Recherche en cours..."):
        try:
            answer = call_n8n(st.session_state["messages"], st.session_state["postal_code"])
        except requests.Timeout:
            answer = "Le serveur met trop de temps à répondre. Veuillez réessayer dans un instant."
        except requests.HTTPError as exc:
            code = exc.response.status_code if exc.response is not None else "inconnu"
            answer = f"Le serveur a renvoyé une erreur HTTP : {code}."
        except requests.RequestException:
            answer = "Erreur lors de l'appel au serveur."
        except ValueError:
            answer = "Le serveur a renvoyé une réponse non valide."

    append_message("assistant", answer)
    with st.chat_message("assistant"):
        st.write(answer)



def main() -> None:
    setup_page()
    init_state()
    render_sidebar()
    render_history()

    user_input = st.chat_input("Votre message...")
    if user_input:
        handle_user_message(user_input)


if __name__ == "__main__":
    main()

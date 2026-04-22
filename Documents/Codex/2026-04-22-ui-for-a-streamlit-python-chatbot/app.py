import os
import re
from dataclasses import dataclass
from typing import Any

import requests
import streamlit as st


def get_setting(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        return os.getenv(name, default)


API_URL = get_setting("ORGANISMES_API_URL")
LLM_URL = get_setting("LLM_API_URL")


@dataclass
class Organisme:
    name: str
    postal_code: str
    city: str = ""
    category: str = "Organisme de l'Etat"
    address: str = ""
    phone: str = ""
    website: str = ""


MOCK_ORGANISMES = [
    Organisme(
        name="Maison France Services",
        postal_code="75013",
        city="Paris",
        category="Accompagnement social",
        address="12 avenue de France",
        phone="01 00 00 00 00",
        website="https://www.france-services.gouv.fr/",
    ),
    Organisme(
        name="Centre communal d'action sociale",
        postal_code="75013",
        city="Paris",
        category="Aide sociale",
        address="3 place d'Italie",
        phone="01 11 11 11 11",
        website="https://www.paris.fr/",
    ),
    Organisme(
        name="Mission locale",
        postal_code="69003",
        city="Lyon",
        category="Insertion et emploi",
        address="24 rue de la Villette",
        phone="04 00 00 00 00",
        website="https://www.missions-locales.org/",
    ),
]


def setup_page() -> None:
    st.set_page_config(
        page_title="Assistant organismes publics",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
            :root {
                --blue-fr: #000091;
                --blue-soft: #f5f5ff;
                --blue-border: #d7d7ff;
                --red-fr: #e1000f;
                --green: #18753c;
                --ink: #161616;
                --muted: #666666;
                --line: #dddddd;
                --surface: #ffffff;
                --surface-alt: #f6f6f6;
            }

            .stApp {
                background:
                    linear-gradient(180deg, rgba(245,245,255,.88) 0%, rgba(255,255,255,1) 28%),
                    var(--surface);
                color: var(--ink);
            }

            .main .block-container {
                padding-top: 1.6rem;
                max-width: 1180px;
            }

            [data-testid="stSidebar"] {
                background: #f6f6f6;
                border-right: 1px solid var(--line);
            }

            .rf-topline {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding: .8rem 0 1.1rem;
                border-bottom: 3px solid var(--blue-fr);
                margin-bottom: 1.3rem;
            }

            .rf-brand {
                display: flex;
                align-items: center;
                gap: .85rem;
                min-width: 0;
            }

            .rf-mark {
                width: 46px;
                height: 46px;
                border: 2px solid var(--blue-fr);
                border-radius: 50%;
                display: grid;
                place-items: center;
                color: var(--blue-fr);
                font-weight: 800;
                background: white;
                flex: 0 0 auto;
            }

            .rf-kicker {
                font-size: .82rem;
                color: var(--muted);
                margin-bottom: .05rem;
            }

            .rf-title {
                margin: 0;
                color: #1e1e1e;
                font-size: clamp(1.55rem, 2.2vw, 2.35rem);
                line-height: 1.08;
                font-weight: 800;
                letter-spacing: 0;
            }

            .rf-status {
                border: 1px solid #b8fec9;
                background: #e3fdeb;
                color: var(--green);
                padding: .4rem .65rem;
                font-size: .85rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .intro-band {
                border-left: 4px solid var(--red-fr);
                background: white;
                padding: 1rem 1.1rem;
                margin-bottom: 1.1rem;
                box-shadow: 0 1px 0 rgba(0,0,0,.04);
            }

            .intro-band p {
                margin: .15rem 0 0;
                color: var(--muted);
            }

            .metric-strip {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: .75rem;
                margin: .9rem 0 1.1rem;
            }

            .metric-tile {
                background: white;
                border: 1px solid var(--line);
                border-radius: 4px;
                padding: .8rem .9rem;
            }

            .metric-tile strong {
                display: block;
                font-size: 1.45rem;
                color: var(--blue-fr);
                line-height: 1.1;
            }

            .metric-tile span {
                color: var(--muted);
                font-size: .84rem;
            }

            .org-card {
                background: white;
                border: 1px solid var(--line);
                border-left: 4px solid var(--blue-fr);
                border-radius: 4px;
                padding: .95rem 1rem;
                margin-bottom: .75rem;
            }

            .org-card h4 {
                margin: 0 0 .3rem;
                font-size: 1.02rem;
                color: var(--ink);
            }

            .org-card p {
                margin: .18rem 0;
                color: var(--muted);
                font-size: .9rem;
            }

            .badge {
                display: inline-flex;
                align-items: center;
                min-height: 1.5rem;
                padding: .15rem .5rem;
                margin-bottom: .45rem;
                background: var(--blue-soft);
                color: var(--blue-fr);
                border: 1px solid var(--blue-border);
                font-size: .78rem;
                font-weight: 700;
            }

            .data-preview {
                background: #1e1e1e;
                color: #f8f8f8;
                border-radius: 4px;
                padding: .9rem;
                font-size: .82rem;
                overflow-x: auto;
                border-top: 4px solid var(--red-fr);
            }

            .stButton > button {
                border-radius: 4px;
                border: 1px solid var(--blue-fr);
                background: var(--blue-fr);
                color: white;
                font-weight: 700;
            }

            .stButton > button:hover {
                border-color: #1212ff;
                background: #1212ff;
                color: white;
            }

            [data-testid="stChatMessage"] {
                border-radius: 6px;
                border: 1px solid rgba(0,0,145,.12);
                background: white;
            }

            @media (max-width: 760px) {
                .rf-topline {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .metric-strip {
                    grid-template-columns: 1fr;
                }

                .rf-status {
                    white-space: normal;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def extract_postal_code(text: str) -> str:
    match = re.search(r"\b(?:0[1-9]|[1-8]\d|9[0-8])\d{3}\b", text)
    return match.group(0) if match else ""


def normalize_organisme(raw: dict[str, Any]) -> Organisme:
    return Organisme(
        name=raw.get("name") or raw.get("nom") or raw.get("denomination") or "Organisme sans nom",
        postal_code=str(raw.get("postal_code") or raw.get("code_postal") or raw.get("cp") or ""),
        city=raw.get("city") or raw.get("ville") or raw.get("commune") or "",
        category=raw.get("category") or raw.get("type") or raw.get("categorie") or "Organisme",
        address=raw.get("address") or raw.get("adresse") or "",
        phone=raw.get("phone") or raw.get("telephone") or "",
        website=raw.get("website") or raw.get("url") or raw.get("site_web") or "",
    )


def fetch_organismes(postal_code: str) -> list[Organisme]:
    if not postal_code:
        return []

    if API_URL:
        try:
            response = requests.get(API_URL, params={"code_postal": postal_code}, timeout=8)
            response.raise_for_status()
            payload = response.json()
            items = payload.get("data", payload if isinstance(payload, list) else payload.get("results", []))
            return [normalize_organisme(item) for item in items]
        except requests.RequestException:
            st.toast("API indisponible: affichage des exemples locaux.")

    return [org for org in MOCK_ORGANISMES if org.postal_code == postal_code]


def build_answer(need: str, postal_code: str, organismes: list[Organisme]) -> str:
    if not postal_code:
        return "Pour chercher les bons organismes, indiquez-moi votre code postal et votre besoin en quelques mots."

    if not organismes:
        return (
            f"Je n'ai pas encore de résultat pour le code postal {postal_code}. "
            "L'interface est prête à interroger l'API dès que son URL sera configurée."
        )

    names = ", ".join(org.name for org in organismes[:3])
    return (
        f"Pour votre besoin ({need or 'à préciser'}) autour du code postal {postal_code}, "
        f"j'ai trouvé {len(organismes)} organisme(s): {names}. "
        "Vous pouvez consulter les fiches à droite pour vérifier l'adresse, le type de service et les coordonnées."
    )


def init_state() -> None:
    st.session_state.setdefault(
        "messages",
        [
            {
                "role": "assistant",
                "content": (
                    "Bonjour, je peux vous orienter vers les organismes publics adaptés. "
                    "Décrivez votre besoin et ajoutez votre code postal."
                ),
            }
        ],
    )
    st.session_state.setdefault("postal_code", "")
    st.session_state.setdefault("need", "")
    st.session_state.setdefault("organismes", [])


def render_header() -> None:
    st.markdown(
        """
        <div class="rf-topline">
            <div class="rf-brand">
                <div class="rf-mark">API</div>
                <div>
                    <div class="rf-kicker">République Française · service d'orientation</div>
                    <h1 class="rf-title">Assistant organismes publics</h1>
                </div>
            </div>
            <div class="rf-status">Accès ouvert · prêt API</div>
        </div>
        <div class="intro-band">
            <strong>Chatbot Streamlit pour relier un besoin utilisateur à des organismes par code postal.</strong>
            <p>Flux prévu: saisie du besoin et du CP, appel API, réponse assistée LLM/RAG, puis sauvegarde structurée.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("Paramètres de recherche")
        postal_code = st.text_input("Code postal", value=st.session_state.postal_code, placeholder="75013")
        need = st.text_area(
            "Besoin",
            value=st.session_state.need,
            placeholder="Ex: aide pour une démarche sociale, emploi, logement...",
            height=110,
        )

        if st.button("Rechercher les organismes", use_container_width=True):
            st.session_state.postal_code = postal_code.strip()
            st.session_state.need = need.strip()
            st.session_state.organismes = fetch_organismes(st.session_state.postal_code)
            answer = build_answer(st.session_state.need, st.session_state.postal_code, st.session_state.organismes)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

        st.divider()
        st.caption("Configuration")
        st.code(
            "ORGANISMES_API_URL\nLLM_API_URL\nSUPABASE_URL\nSUPABASE_KEY",
            language="text",
        )
        st.caption("Les noms de champs API acceptés incluent: name, nom, code_postal, cp, ville, adresse, telephone.")


def render_metrics() -> None:
    count = len(st.session_state.organismes)
    cp = st.session_state.postal_code or "Non renseigné"
    api_state = "Connectée" if API_URL else "Exemple local"
    st.markdown(
        f"""
        <div class="metric-strip">
            <div class="metric-tile"><strong>{count}</strong><span>Organismes trouvés</span></div>
            <div class="metric-tile"><strong>{cp}</strong><span>Code postal ciblé</span></div>
            <div class="metric-tile"><strong>{api_state}</strong><span>Source de données</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_organismes() -> None:
    st.subheader("Résultats API")

    if not st.session_state.organismes:
        st.info("Aucun organisme chargé. Lancez une recherche avec un code postal.")
        return

    for org in st.session_state.organismes:
        st.markdown(
            f"""
            <div class="org-card">
                <span class="badge">{org.category}</span>
                <h4>{org.name}</h4>
                <p><strong>Code postal:</strong> {org.postal_code} · {org.city or "Ville non renseignée"}</p>
                <p><strong>Adresse:</strong> {org.address or "Non renseignée"}</p>
                <p><strong>Téléphone:</strong> {org.phone or "Non renseigné"}</p>
                <p><strong>Site:</strong> {org.website or "Non renseigné"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_schema_preview() -> None:
    preview = {
        "need": st.session_state.need,
        "postal_code": st.session_state.postal_code,
        "organismes": [org.__dict__ for org in st.session_state.organismes[:2]],
        "llm_response": "Réponse construite à partir du besoin, du CP et du contexte RAG.",
        "saved_to_supabase": False,
    }
    st.subheader("Payload prévu")
    st.json(preview, expanded=False)
    st.caption("Ce format peut être envoyé à Supabase après validation de la réponse.")


def render_chat() -> None:
    st.subheader("Conversation")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Décrivez votre besoin avec votre code postal...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    postal_code = extract_postal_code(prompt) or st.session_state.postal_code
    need = re.sub(r"\b(?:0[1-9]|[1-8]\d|9[0-8])\d{3}\b", "", prompt).strip(" ,.;")

    st.session_state.postal_code = postal_code
    st.session_state.need = need or st.session_state.need
    st.session_state.organismes = fetch_organismes(postal_code)

    answer = build_answer(st.session_state.need, postal_code, st.session_state.organismes)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()


def main() -> None:
    setup_page()
    init_state()
    render_header()
    render_sidebar()
    render_metrics()

    left, right = st.columns([1.25, 1], gap="large")
    with left:
        render_chat()
    with right:
        render_organismes()
        render_schema_preview()


if __name__ == "__main__":
    main()

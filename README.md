# Le Relais - Application Streamlit

Ce projet est une interface de chatbot d'accompagnement social construite avec **Streamlit**. L'application, nommée **Le Relais**, aide l'utilisateur a identifier des organismes locaux et des aides adaptees selon sa situation et son code postal.

L'interface est en francais et envoie les messages vers un webhook `n8n` execute en local.

## Fonctionnalites

- Interface de discussion avec historique conserve pendant la session
- Saisie du code postal dans la barre laterale pour personnaliser les resultats
- Bouton de reinitialisation de la conversation
- Exemples de questions pour guider l'utilisateur
- Connexion a un workflow `n8n` local pour generer les reponses

## Fichier principal

- `Main_App_Streamlit_V6.py`

## Prerequis

Vous aurez besoin de :

- Python 3.9 ou plus
- `streamlit`
- `requests`
- une instance locale de `n8n`
- l'image `Chatbot.png` dans le meme dossier que l'application, ou un chemin mis a jour dans le code

## Installation

```bash
pip install streamlit requests
```

## Lancer l'application

Demarrer l'application Streamlit :

```bash
streamlit run Main_App_Streamlit_V6.py
```

## Lancer n8n

L'application attend ce webhook :

```text
http://localhost:5678/webhook/DemoDay2
```

Demarrer `n8n` en local avant d'utiliser le chatbot :

```bash
npx n8n start
```

## Fonctionnement

1. L'utilisateur renseigne son code postal dans la barre laterale.
2. L'utilisateur envoie un message dans l'interface de chat.
3. L'application transmet l'historique de la conversation ainsi que le code postal au webhook `n8n`.
4. Le webhook renvoie une reponse qui est ensuite affichee dans la discussion.

Charge utile envoyee a `n8n` :

```json
{
  "messages": [
    { "role": "user", "content": "..." }
  ],
  "CP": "69000"
}
```

## Remarques

- Si aucun code postal n'est saisi, l'envoi du message est bloque et un avertissement s'affiche.
- L'historique des messages est stocke dans `st.session_state["messages"]`.
- L'interface contient un style personnalise pour la barre laterale ainsi qu'un texte d'accueil en francais.
- Si le webhook n'est pas disponible, l'application affiche une erreur de connexion dans le chat.

## Exemples d'usage

- Trouver des aides pour payer son logement
- Rechercher une aide alimentaire a proximite
- Identifier des pistes d'accompagnement pour un emploi etudiant

## Contexte du projet

Cette application semble avoir ete concue pour une demonstration ou un prototype local dans lequel :

- Streamlit fournit l'interface utilisateur
- `n8n` orchestre la logique de traitement
- les recommandations sont personnalisees a partir du code postal de l'utilisateur

## Pistes d'amelioration

- ajouter un fichier `requirements.txt`
- configurer l'URL du webhook via des variables d'environnement
- valider la reponse du webhook avant affichage
- ameliorer la gestion des erreurs si la reponse n'est pas en JSON
- ajouter une section de deploiement

## Licence

Aucune licence n'est actuellement specifiee.



#English
This project is a Streamlit-based social assistance chatbot interface named Le Relais. It helps users identify local organizations and support options based on their situation and postal code.

The app is written in French and sends chat requests to an n8n webhook running locally.

Features
Streamlit chat interface with persistent conversation history
Postal-code input in the sidebar for localized results
Reset button to clear the conversation
Example prompts to guide first-time users
Integration with a local n8n workflow for response generation
Main File
Main_App_Streamlit_V6.py
Requirements
You will need:

Python 3.9+
streamlit
requests
A local n8n instance
The image asset Chatbot.png in the same folder as the app, or an updated path in the code
Install
pip install streamlit requests
Run the App
Start the Streamlit app:

streamlit run Main_App_Streamlit_V6.py
Run n8n
The app expects this webhook endpoint:

http://localhost:5678/webhook/DemoDay2
Start n8n locally before using the chatbot:

npx n8n start
How It Works
The user enters a postal code in the sidebar.
The user sends a message through the chat input.
The app sends the conversation history and postal code to the n8n webhook.
The webhook returns a response that is displayed in the chat.
Payload sent to n8n:

{
  "messages": [
    { "role": "user", "content": "..." }
  ],
  "CP": "69000"
}
Notes
If no postal code is entered, the app blocks chat submission and shows a warning.
Conversation history is stored in st.session_state["messages"].
The UI includes custom sidebar styling and onboarding text in French.
If the webhook is unavailable, the app shows a connection error in the chat.
Example Use Cases
Finding housing assistance
Locating food aid nearby
Exploring job-related support for students
Project Context
This app appears to be designed for a local demo or prototype where:

Streamlit provides the frontend
n8n orchestrates backend logic
localized support recommendations are generated from the user's postal code
Suggested Improvements
Add a requirements.txt
Add environment-based configuration for the webhook URL
Validate webhook responses before rendering
Improve error handling for non-JSON responses
Add deployment instructions
License
No license is currently specified.
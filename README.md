# Assistant Social - Streamlit

Application Streamlit en français pour orienter un utilisateur vers des organismes publics ou sociaux à partir d'un besoin et d'un code postal.

Le projet combine :

- une interface chatbot Streamlit ;
- un webhook n8n pour traiter la demande ;
- une recherche par code postal ;
- un dossier de PDF pour les documents sources du projet ;
- une configuration locale par fichier `.env`.

## Structure du projet

```text
jedha_group2/
├── raw_pdfs/
│   └── documents sources du projet
├── streamlit/
│   ├── app.py
│   ├── main_app_streamlit_v2.py
│   └── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── 00-Understanding_RAG.ipynb
```

## Installation

Depuis la racine du projet :

```bash
cd C:\Users\ron\Documents\project\jedha\jedha_group2
```

Installer les dépendances :

```bash
pip install -r streamlit/requirements.txt
```

## Configuration locale

Le vrai fichier `.env` reste local et ne doit pas être poussé sur GitHub.

Créer le fichier local :

```cmd
copy .env.example .env
```

Puis remplir les variables :

```env
N8N_WEBHOOK_URL=
ORGANISMES_API_URL=
LLM_API_URL=
SUPABASE_URL=
SUPABASE_KEY=
```

La variable principale utilisée par `main_app_streamlit_v2.py` est :

```env
N8N_WEBHOOK_URL=
```

## Lancer l'application

Depuis la racine du projet :

```bash
streamlit run streamlit/main_app_streamlit_v2.py
```

Ancienne version :

```bash
streamlit run streamlit/app.py
```

## Ajouter des PDF

Placer les documents PDF dans :

```text
raw_pdfs/
```

Puis les ajouter à Git si les documents peuvent être partagés dans le dépôt :

```bash
git add raw_pdfs
git commit -m "Add project PDFs"
git push origin main
```

Si les PDF sont privés, volumineux ou protégés par droits, ne pas les pousser directement dans GitHub.

## Variables et secrets

Ne jamais pousser le fichier `.env`.

Le dépôt contient uniquement :

```text
.env.example
```

Chaque membre du groupe doit créer son propre `.env` local à partir du modèle.

## Fonctionnement général

1. L'utilisateur saisit son besoin et son code postal.
2. L'application Streamlit envoie la demande au webhook n8n.
3. Le webhook peut appeler les APIs, le RAG ou le modèle LLM.
4. La réponse est affichée dans l'interface.
5. Les organismes trouvés et le payload peuvent être visualisés dans l'application.

## Commandes Git utiles

Vérifier la branche :

```bash
git branch
```

Vérifier les changements :

```bash
git status
```

Ajouter les fichiers sûrs :

```bash
git add README.md .env.example .gitignore streamlit/main_app_streamlit_v2.py
```

Commit :

```bash
git commit -m "Update project documentation"
```

Push :

```bash
git push origin main
```

## Avertissement

Ce projet est réalisé dans un cadre pédagogique. Les réponses de l'assistant ne remplacent pas un avis professionnel, administratif, juridique, médical ou social.

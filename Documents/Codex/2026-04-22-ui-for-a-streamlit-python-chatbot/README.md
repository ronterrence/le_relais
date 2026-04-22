# Assistant Streamlit pour organismes publics

Interface Streamlit en français, inspirée des codes visuels de data.gouv.fr, pour orienter un utilisateur vers des organismes publics à partir d'un besoin et d'un code postal.

## Lancer l'application

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Variables attendues

Dans `.streamlit/secrets.toml`, vous pouvez configurer:

```toml
ORGANISMES_API_URL = "https://exemple.fr/api/organismes"
LLM_API_URL = "https://exemple.fr/api/chat"
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "..."
```

L'API organismes peut retourner une liste directe, ou un objet contenant `data` ou `results`.
Les champs reconnus incluent `name`, `nom`, `denomination`, `postal_code`, `code_postal`, `cp`, `city`, `ville`, `commune`, `address`, `adresse`, `phone`, `telephone`, `website`, `url` et `site_web`.

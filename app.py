import streamlit as st
from generator import generate_prompt, load_error

st.set_page_config(page_title="Prompt Generator", page_icon="🤖", layout="centered")

st.markdown("<h1 style='text-align: left;'>Prompt Generator for ChatGPT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Générez automatiquement des prompts efficaces, clairs et adaptés à vos besoins</p>", unsafe_allow_html=True)

PROMPT_CATEGORIES = {
    "Marketing": "Tu es un expert en marketing digital et communication persuasive.",
    "Storytelling": "Tu es un écrivain créatif spécialisé dans la narration immersive.",
    "Code": "Tu es un développeur expérimenté qui crée des prompts techniques pour générer du code clair et fonctionnel.",
    "Étude": "Tu es un professeur pédagogue, expert en formulation de questions et d'exercices académiques.",
}

DETAIL_LEVELS = {
    "Simple": "Le prompt doit être court, direct et facile à comprendre.",
    "Moyen": "Le prompt doit fournir des instructions complètes mais concises.",
    "Très détaillé": "Le prompt doit inclure un rôle, un objectif, un contexte et des consignes structurées.",
}

PROMPT_PATTERNS = {
    "Agis comme...": "Crée un prompt qui commence par 'Agis comme...' pour établir un rôle clair.",
    "Étapes à suivre": "Formule un prompt qui demande une réponse étape par étape.",
    "Objectif clair": "Structure un prompt autour d'un objectif explicite à atteindre.",
    "Réponse avec contraintes": "Génère un prompt demandant une réponse avec des contraintes précises (longueur, ton, format).",
    "Créatif / roleplay": "Formule un prompt immersif avec un ton ou une personnalité spécifique.",
}

with st.sidebar:
    st.header("Paramètres du prompt")
    category = st.selectbox("📌 Type de prompt", list(PROMPT_CATEGORIES.keys()))
    style = st.selectbox("🎛️ Niveau de détail", list(DETAIL_LEVELS.keys()))
    pattern = st.selectbox("🧠 Modèle de génération", list(PROMPT_PATTERNS.keys()))
    st.caption(PROMPT_PATTERNS[pattern])

st.markdown("### Quel est votre besoin ?")
user_input = st.text_area("", placeholder="Ex : Je veux ouvrir un foodtruck à Paris", height=150)

if st.button("✨ Générer le prompt"):
    if load_error is not None:
        st.error(f"Le modèle n'a pas pu être chargé : {load_error}")
    elif not user_input.strip():
        st.warning("Veuillez d'abord renseigner votre besoin.")
    else:
        with st.spinner("Génération du prompt en cours..."):
            result = generate_prompt(category, style, pattern, user_input)
        st.success("✅ Prompt généré avec succès !")
        st.markdown("### 📋 Résultat")
        st.code(result, language="markdown")

        st.download_button("📥 Télécharger le prompt", result, file_name="prompt.txt", mime="text/plain")

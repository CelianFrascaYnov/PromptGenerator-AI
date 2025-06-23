import streamlit as st
import random
from generator import generate_prompt, load_error

st.set_page_config(page_title="Prompt Generator", page_icon="🤖", layout="centered")

# Initialisation de l'historique et de l'état de génération
if 'history' not in st.session_state:
    st.session_state.history = []
if 'generating' not in st.session_state:
    st.session_state.generating = False

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

PLACEHOLDER_EXAMPLES = [
    "Je veux ouvrir un foodtruck à Paris",
    "Je cherche une idée de vidéo TikTok virale pour une app mobile",
    "Je veux une histoire de science-fiction dans un monde post-apocalyptique",
    "J’ai besoin d’un script Python pour automatiser l’envoi de mails",
    "Je veux une fiche de révision sur la mémoire à long terme",
    "Génère une stratégie marketing pour une marque de vêtements éthiques",
    "Crée un quiz de 10 questions sur les civilisations anciennes",
    "Je veux un mini-jeu Flutter avec un bouton et un score",
    "Crée une explication simple du théorème de Pythagore",
    "Rédige une scène dramatique entre deux frères ennemis"
]

generating = st.session_state.generating

with st.sidebar:
    st.header("Paramètres du prompt")
    category = st.selectbox("📌 Type de prompt", list(PROMPT_CATEGORIES.keys()))
    style = st.selectbox("🎛️ Niveau de détail", list(DETAIL_LEVELS.keys()))
    pattern = st.selectbox("🧠 Modèle de génération", list(PROMPT_PATTERNS.keys()))
    st.caption(PROMPT_PATTERNS[pattern])

st.markdown("### Quel est votre besoin ?")
if "random_placeholder" not in st.session_state:
    st.session_state.random_placeholder = random.choice(PLACEHOLDER_EXAMPLES)

user_input = st.text_area("", placeholder=st.session_state.random_placeholder, height=150)


if st.button("✨ Générer le prompt", disabled=generating):
    if load_error is not None:
        st.error(f"Le modèle n'a pas pu être chargé : {load_error}")
    elif not user_input or not user_input.strip():
        st.warning("Veuillez d'abord renseigner votre besoin.")
    else:
        st.session_state.generating = True
        with st.spinner("Génération du prompt en cours..."):
            result = generate_prompt(category, style, pattern, user_input)
        st.session_state.generating = False

        st.success("✅ Prompt généré avec succès !")
        st.markdown("### 📋 Résultat")
        st.code(result, language="markdown")

        st.download_button("📥 Télécharger le prompt", result, file_name="prompt.txt", mime="text/plain")

        st.session_state.history.append({
            "prompt": result,
            "input": user_input,
            "category": category,
            "style": style,
            "pattern": pattern,
        })

# Historique
if st.session_state.history:
    st.markdown("### 📚 Historique")
    for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
        with st.expander(f"🔹 Prompt #{len(st.session_state.history) - i + 1}"):
            st.markdown(f"**Input utilisateur :** {item['input']}")
            st.markdown(f"**Catégorie :** {item['category']}")
            st.markdown(f"**Niveau de détail :** {item['style']}")
            st.markdown(f"**Modèle :** {item['pattern']}")
            st.code(item['prompt'], language="markdown")

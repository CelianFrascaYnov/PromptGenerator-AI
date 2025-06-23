import streamlit as st

from generator import generate_prompt, load_error

st.title("Prompt Generator for ChatGPT")

PROMPT_CATEGORIES = [
    "Marketing",
    "Storytelling",
    "Code",
    "Étude",
]

DETAIL_LEVELS = [
    "Simple",
    "Moyen",
    "Très détaillé",
]

with st.sidebar:
    st.header("Paramètres")
    category = st.selectbox("Type de prompt", PROMPT_CATEGORIES)
    style = st.selectbox("Niveau de détail", DETAIL_LEVELS)

user_input = st.text_area("Exprimez votre besoin :", height=200)

if st.button("Générer le prompt"):
    if load_error is not None:
        st.error(f"Le modèle n'a pas pu être chargé : {load_error}")
    else:
        if not user_input.strip():
            st.warning("Veuillez d'abord remplir le champ de besoin utilisateur.")
        else:
            with st.spinner("Génération en cours..."):
                result = generate_prompt(category, style, user_input)
            st.subheader("Prompt généré")
            st.code(result)

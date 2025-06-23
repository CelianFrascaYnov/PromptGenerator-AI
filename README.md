# Prompt Generator for ChatGPT

Cette application Streamlit permet de générer automatiquement des prompts optimisés pour ChatGPT à partir d'un besoin exprimé par l'utilisateur. Elle utilise le modèle **Mistral 7B Instruct v0.3** via l'API **Hugging Face Inference**.

## 🧠 Fonctionnalités

- Choix du **type de prompt** (marketing, storytelling, code, étude)
- Choix du **niveau de détail** et d’un **modèle de prompt engineering**
- Historique des prompts générés
- Blocage du bouton pendant la génération
- Téléchargement du prompt généré

## 🚀 Installation

1. Clonez le dépôt et installez les dépendances :

```bash
pip install -r requirements.txt
```
2. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API Hugging Face :

```
HUGGINGFACE_API_KEY=your_api_key_here
```

## 🏃‍♂️ Lancer l'application
```bash
streamlit run app.py
```
l'interface sera accessible à l'adresse `http://localhost:8501`.

## 🔗 Modèle utilisé
Le modèle utilisé pour la génération de prompts est **Mistral 7B Instruct v0.3** disponible sur Hugging Face. lien: [Mistral 7B Instruct v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)

## 📦 Dépendances
- `streamlit`
- `transformers`
- `torch`
- `huggingface_hub`
- `python-dotenv`

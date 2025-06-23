# Prompt Generator for ChatGPT

Cette application Streamlit permet de générer automatiquement des prompts optimisés pour ChatGPT à partir d'un besoin exprimé par l'utilisateur.

## Installation

1. Clonez le dépôt puis installez les dépendances :

```bash
pip install -r requirements.txt
```

Le téléchargement du modèle peut prendre quelques minutes lors du premier lancement.

Par défaut, l'application utilise le modèle HuggingFace `gpt-neo-125M`. Les résultats peuvent rester succincts; n'hésitez pas à augmenter le nombre de tokens générés ou à tester avec un autre modèle si disponible.

## Utilisation

Exécutez l'application Streamlit :

```bash
python -m streamlit run app.py
```

Une interface web s'ouvre dans votre navigateur. Sélectionnez le type de prompt, le niveau de détail souhaité et saisissez votre besoin. Cliquez sur **Générer le prompt** pour obtenir un texte prêt à être utilisé avec ChatGPT.

## Dépendances

- [Streamlit](https://streamlit.io/)
- [Transformers](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)
